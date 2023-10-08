import asyncio
import logging
import aio_pika
from abc import ABC
from base.settings import Settings
from base.amqp.connection import get_connection
from base.amqp.exchange import create_exchange
import openai
import re
import tiktoken
import json
from database.connection import get_db
from database.dao import (
    get_layer_state_by_name,
    get_layer_config,
    get_active_ancestral_prompt,
)
from database.dao_models import LayerConfigModel, AncestralPromptModel


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseLayer(ABC):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.loop = asyncio.get_event_loop()
        self.connection = None
        self.channel = None
        self.llm_messages = []
        self.ancestral_prompt: AncestralPromptModel
        self.layer_config: LayerConfigModel
        self._fetch_layer_config()
        self._fetch_ancestral_prompt()

    async def data_bus_message_handler(self, message: aio_pika.IncomingMessage):
        try:
            if self.settings.debug:
                self.wait_for_signal()

            with get_db() as session:
                await self._process_message(message, session, "Data Bus")
                await message.ack()
        except:
            await message.nack()

    async def control_bus_message_handler(self, message: aio_pika.IncomingMessage):
        try:
            if self.settings.debug:
                await self.wait_for_signal()

            with get_db() as session:
                await self._process_message(message, session, "Control Bus")
                await message.ack()
        except:
            await message.nack()

    async def wait_for_signal(self):
            while True:
                with get_db() as session:

                    process_messages = get_layer_state_by_name(
                        db=session,
                        layer_name=self.settings.role_name,
                    )

                if process_messages:
                    break
                await asyncio.sleep(3)

    async def _process_message(
        self, message: aio_pika.IncomingMessage, source_bus: str
    ):
        self._fetch_layer_config()
        self._fetch_ancestral_prompt()

        await self._handle_bus_message(
            layer_config=self.layer_config,
            message=message,
            source_bus=source_bus,
        )

    def _reason(
        self,
        input: str,
        source_bus: str,
    ):
        reasoning_prompt = f"""
# You Received a MESSAGE From the SOURCE BUS
## MESSAGE
{input}

## SOURCE BUS
{source_bus}
"""
        system_message = f"""
{self.layer_config.prompts.identity}

{self.ancestral_prompt}

{self.layer_config.prompts.reasoning}
"""
        reasoning_messages = (
            [
                {"role": "system", "content": system_message},
            ]
            + self.llm_messages
            + [{"role": "user", "content": reasoning_prompt}]
        )

        reasoning_response = openai.ChatCompletion.create(
            messages=reasoning_messages,
            **self.layer_config.llm_model_parameters.model_dump(
                exclude_none=True,
                exclude_unset=True,
            ),
        )
        results = reasoning_response.choices[0].message
        return results

    async def _handle_bus_message(self, message: aio_pika.IncomingMessage, source_bus):
        reasoning_completion = self._reason()

        data_bus_message, control_bus_message = self._determine_action(
            source_bus,
            reasoning_completion,
        )

        if self._determine_none(data_bus_message) != "none":
            await self._publish(
                queue_name=self.settings.data_bus_pub_queue,
                message=data_bus_message,
                destination_bus="Data Bus",
                source_bus=source_bus,
                input_message=message,
                reasoning_message=reasoning_completion,
            )
            self.llm_messages.append(f"sent {control_bus_message} to control bus")

        if self._determine_none(control_bus_message) != "none":
            await self._publish(
                queue_name=self.settings.control_bus_pub_queue,
                message=control_bus_message,
                destination_bus="Control Bus",
                source_bus=source_bus,
                input_message=message,
                reasoning_message=reasoning_completion,
            )
            self.llm_messages.append(f"sent {control_bus_message} to control bus")

    def _determine_action(
        self,
        source_bus,
        reasoning_completion,
    ):
        data_bus_prompt = self._get_action_prompt(
            source_bus=source_bus,
            destination_bus="Data Bus",
            reasoning_completion=reasoning_completion,
        )
        control_bus_prompt = self._get_action_prompt(
            source_bus=source_bus,
            destination_bus="Control Bus",
            reasoning_completion=reasoning_completion,
        )

        data_bus_action = (
            [
                {
                    "role": "system",
                    "content": f"{self.layer_config.prompts.identity}\n{self.layer_config.prompts.reasoning}",
                },
            ]
            + self.llm_messages
            + [{"role": "user", "content": data_bus_prompt}]
        )

        control_bus_action = (
            [
                {
                    "role": "system",
                    "content": f"{self.layer_config.prompts.identity}\n{self.layer_config.prompts.reasoning}",
                },
            ]
            + self.llm_messages
            + [{"role": "user", "content": control_bus_prompt}]
        )

        data_bus_action_completion = (
            openai.ChatCompletion.create(
                model=self.layer_config.llm_model_name,
                messages=data_bus_action,
                **self.layer_config.llm_model_parameters,
            )
            .choices[0]
            .message
        )

        control_bus_action_completion = (
            openai.ChatCompletion.create(
                model=self.layer_config.llm_model_name,
                messages=control_bus_action,
                **self.layer_config.llm_model_parameters,
            )
            .choices[0]
            .message
        )

        return data_bus_action_completion, control_bus_action_completion
    
    def _determine_none(self, input_text):
        match = re.search(r"\[Message\]\n(none)", input_text)

        if match:
            return "none"

        return input_text
    
    async def _publish(
        self,
        queue_name,
        message,
        destination_bus,
        source_bus,
        input_message: aio_pika.IncomingMessage,
        reasoning_message,
    ):
        exchange = await create_exchange(
            connection=self.connection,
            queue_name=queue_name,
        )

        headers = {
            "source_bus": source_bus,
            "parent_message_id": input_message.message_id,
            "destination_bus": destination_bus,
            "layer_name": self.settings.role_name,
            "llm_messages": json.dump(self.llm_messages),
            "config_id": self.layer_config.config_id,
            "input": input_message.body.decode(),
            "reasoning": json.dump(reasoning_message),
        }

        message_body = aio_pika.Message(
            body=message.encode(),
            headers=headers,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            content_type="text/plain",
        )

        logger.info(f"publishing {queue_name=}, {destination_bus=}, {source_bus=}")

        await exchange.publish(
            message_body,
            routing_key=queue_name,
        )

    def _get_action_prompt(
        self,
        source_bus: str,
        destination_bus: str,
        reasoning_completion: str
    ):
        action_prompt = f"""
# Given Your Role as the {self.settings.role_name} in the ACE framework
Consider the INPUT, YOUR REASONING about it, and BUS RULES to decide what, if any, message you should place on the {destination_bus}

## INPUT
Input source bus = {source_bus}

## YOUR REASONING
{reasoning_completion}

## BUS RULES
{self.layer_config.prompts.bus}
"""
        return action_prompt

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

    def _compact_llm_messages(self):
        token_count = 0
        for message in self.llm_messages:
            token_count += self._count_tokens(message)
        logger.info(f"Current {token_count=}")
        if token_count > self.settings.memory_max_tokens:
            logger.info("compacting initiated...")
            self._update_llm_messages()
            token_count = self._count_tokens(self.llm_messages[0])
            logger.info(f"After compaction memory {token_count=}")
        else:
            logger.info("No compaction required")

    def _update_llm_messages(self):
        openai.api_key = self.settings.openai_api_key
        identity = {"role": "system", "content": self.layer_config.prompts.identity}
        summarization_prompt = {"role": "user", "content": p.memory_compaction_prompt}

        conversation = [identity] + self.llm_messages + [summarization_prompt]

        completion = openai.ChatCompletion.create(
            model=self.settings.model,
            messages=conversation,
            temperature=self.settings.temperature,
        )
        self.llm_messages = [completion.choices[0].message]

    def _count_tokens(self, message: str) -> int:
        encoding = tiktoken.encoding_for_model(self.settings.model)

        logger.info(f"{message=}")

        num_tokens = len(encoding.encode(message["content"]))
        return num_tokens

    def _fetch_layer_config(self):
        with get_db() as db:
            self.layer_config = get_layer_config(
                db=db,
                layer_name=self.settings.role_name,
            )

    def _fetch_ancestral_prompt(self):
        with get_db() as db:
            self.ancestral_prompt = get_active_ancestral_prompt(db=db)

    async def _run_layer(self):
        logger.info(f"Running {self.settings.role_name}")
        await self._connect()
        await self._subscribe()
        logger.info(
            f"{self.settings.role_name} Subscribed to {self.settings.data_bus_sub_queue} and {self.settings.control_bus_sub_queue}"
        )

    def run(self):
        self.loop.create_task(self._run_layer())
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()
