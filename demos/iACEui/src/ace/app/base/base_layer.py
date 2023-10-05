import asyncio
import logging
import aio_pika
from abc import ABC
from base.settings import Settings
import base.prompts as p
from base.amqp.connection import get_connection
from base.amqp.exchange import create_exchange
import time
import openai
import re
import tiktoken
import json
from database.connection import get_db
from database.dao import (
    get_layer_state_by_name, 
    get_layer_config, 
    update_layer_state,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseLayer(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings
        self.loop = asyncio.get_event_loop()
        self.connection = None
        self.channel = None
        self.llm_messages = []
        self.identity = None
        self.bus_prompt = None
        self.reasoning_prompt = None

        with get_db as session:
            self.layer_config = get_layer_config(
                db=session, 
                layer_name=self.settings.role_name, 
                active=True,
            )

        self.identity = self.layer_config.prompts.get('identity')
        self.reasoning_prompt = self.layer_config.prompts.get('reasoning_prompt')
        self.bus_message_prompt = self.layer_config.prompts.get('bus_prompt')
        self.config_id = self.layer_config.get('config_id')

    async def data_bus_message_handler(self, message: aio_pika.IncomingMessage):
        process_messages = True
        if self.settings.debug:
            process_messages = self.wait_for_signal()

        if process_messages:
            with get_db() as session:
                await self._process_message(message, session, "Data Bus")
                await message.ack()
        else:
            await message.nack()

    async def control_bus_message_handler(self, message: aio_pika.IncomingMessage):
        process_messages = True
        if self.settings.debug:
            process_messages = self.wait_for_signal()

        if process_messages:
            with get_db() as session:
                await self._process_message(message, session, "Control Bus")
                await message.ack()
        else:
            await message.nack()

    def wait_for_signal(self):
        with get_db() as session:
            while True:
                process_messages = get_layer_state_by_name(
                    db=session,
                    layer_name=self.settings.role_name,
                )
                if process_messages:
                    break
                time.sleep(3)
        return process_messages

    async def _process_message(self, message, session, source):
        if self.settings.debug:
            process_messages = False
            update_layer_state(
                db=session,
                process_messages=process_messages,
                layer_name=self.settings.role_name,
            )

        layer_config = get_layer_config(
            db=session,
            layer_name=self.settings.role_name,
            active=True,
        )
        await self._handle_bus_message(
            layer_config=layer_config,
            message=message,
            source=source,
        )

    def _get_bus_messages(self):
        bus_message_response = self._generate_completion(self.bus_prompt)
        data_bus_meessage = self._extract_section(
            input_string=bus_message_response, 
            section_name='Data Bus Message',
        )
        control_bus_meessage = self._extract_section(
            input_string=bus_message_response,
            section_name='Data Bus Message',
        )

        return data_bus_meessage, control_bus_meessage

    def _extract_section(input_string, section_name):
        match = re.search(fr'\[{re.escape(section_name)}\]([^\[]*)', input_string)
        return match.group(1).strip() if match else None

    async def _handle_bus_message(self, message, source):
        # reason about the message that came from the source bus.
        reasoning_response = self._generate_completion("\n".join(
            self.reasoning_prompt,
            f"[{source}]",
            {message.body.decode()})
        )

        # request the messages to publish if any
        data_bus_message, control_bus_message = self._get_bus_messages()

        if data_bus_message:
            await self._publish(
                queue_name=self.settings.data_bus_pub_queue,
                message=data_bus_message,
                destination_bus="Data Bus",
                source_bus=source,
                input_message=message,
                reasoning_message=reasoning_response,
            )
        if control_bus_message:
            await self._publish(
                queue_name=self.settings.control_bus_pub_queue,
                message=control_bus_message,
                destination_bus="Control Bus",
                source_bus=source,
                input_message=message,
                reasoning_message=reasoning_response,
            )

    async def _connect(self):
        self.connection = await get_connection(
            loop=self.loop,
            amqp_host_name=self.settings.amqp_host_name,
            username=self.settings.amqp_username,
            password=self.settings.amqp_password,
            role_name=self.settings.role_name,
        )
        self.channel = await self.connection.channel()
        logger.info(f"{self.settings.role_name} connection established...")

    async def _subscribe(self):
        nb_queue = await self.channel.declare_queue(
            self.settings.data_bus_sub_queue, 
            durable=True,
        )
        sb_queue = await self.channel.declare_queue(
            self.settings.control_bus_sub_queue, 
            durable=True,
        )

        await nb_queue.consume(self.data_bus_message_handler)
        await sb_queue.consume(self.control_bus_message_handler)

    def _generate_completion(self, new_message, role="user"):
        openai.api_key = self.settings.openai_api_key
        identity = {"role": "system", "content": self.identity}
        new_prompt = {"role": role, "content": new_message}

        conversation = ([identity] + self.llm_messages + [new_prompt])

        completion = openai.ChatCompletion.create(
            model=self.settings.model,
            messages=conversation,
            temperature=self.settings.temperature,
        )
        response = completion.choices[0].message

        if role in ["user", "assistant"]:
            self.llm_messages.append(new_prompt)
            self.llm_messages.append(response)
            self._compact_llm_messages()

        return response["content"]

    def _compact_llm_messages(self):
        token_count = 0
        for message in self.llm_messages:
            token_count += self._count_tokens(message)
        logger.info(f"Current {token_count=}")
        if token_count > self.settings.memory_max_tokens:
            logger.info("compacting initiated...")
            self._update_llm_messages()
            token_count = self._count_tokens(self.llm_messages[0])
            logger.info("After compaction memory {token_count=}")
        else:
            logger.info("No compaction required")

    def _update_llm_messages(self):
        openai.api_key = self.settings.openai_api_key
        identity = {"role": "system", "content": self.identity}
        summarization_prompt = {"role": "user", "content": p.memory_compaction_prompt}

        conversation = ([identity] + self.llm_messages + [summarization_prompt])

        completion = openai.ChatCompletion.create(
                model=self.settings.model,
                messages=conversation,
                temperature=self.settings.temperature,
            )
        self.llm_messages = [completion.choices[0].message]

    def _count_tokens(self, message: str) -> int:
        encoding  = tiktoken.encoding_for_model(self.settings.model)

        logger.info(f"{message=}")

        num_tokens = len(encoding.encode(message["content"]))
        return num_tokens

    async def _publish(
        self,
        queue_name,
        message, 
        destination_bus,
        source_bus,
        input_message,
        reasoning_message,
    ):
        if self._determine_none(message) != 'none':
            exchange = await create_exchange(
                connection=self.connection,
                queue_name=queue_name,
            )

            headers = {
                'source_bus': source_bus,
                'destination_bus': destination_bus,
                'layer_name': self.settings.role_name,
                'llm_messages': json.dumps(self.llm_messages),
                'model': self.settings.model,
                'config_id': self.config_id,
                'input': input_message.body.decode(),
                'reasoning': reasoning_message,
            }

            message_body = aio_pika.Message(
                body=message.encode(),
                headers=headers,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type='text/plain',
            )

            logger.info(f"publishing {queue_name=}, {destination_bus=}, {source_bus=}")

            await exchange.publish(
                message_body,
                routing_key=queue_name,
            )

    def _determine_none(self, input_text):
        match = re.search(r'\[Message\]\n(none)', input_text)

        if match:
            return 'none'

        return input_text

    async def _run_layer(self):
        logger.info(f"Running {self.settings.role_name}")
        await self._connect()
        await self._subscribe()
        logger.info(f"{self.settings.role_name} Subscribed to {self.settings.data_bus_sub_queue} and {self.settings.control_bus_sub_queue}")

    def run(self):
        self.loop.create_task(self._run_layer())
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()


# def closest_match(input_str: str, options: List[str]):
#     scores = [fuzz.ratio(input_str, option) for option in options]
#     return options[scores.index(max(scores))]

