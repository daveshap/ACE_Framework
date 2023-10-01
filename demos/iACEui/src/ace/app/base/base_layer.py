import asyncio
import logging
import aio_pika
from abc import ABC, abstractmethod
from base.settings import Settings
import base.prompts as p
from base.amqp.connection import get_connection
from base.amqp.exchange import create_exchange
import time
import openai
from typing import List


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseLayer(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings
        self.loop = asyncio.get_event_loop()
        self.connection = None
        self.channel = None
        self.primary_directive = self.get_primary_directive()

        self.primary_directive_messages=[
            {"role": "system", "content": self.primary_directive},
            {"role": "user", "content": "Give me a brief summary about who or what you are."}
        ]

        logger.info(f"setting {self.settings.role_name} Layer's mission")
        chat_completion = self._generate_multi_message_completion(self.primary_directive_messages)
        logger.info(chat_completion)


    @abstractmethod
    def get_primary_directive(self):
        pass

    # Override this function in your subclass, the default behavior here is to confirm the system is up and running
    async def northbound_message_handler(self, message: aio_pika.IncomingMessage):
        msg = message.body.decode()
        logger.info(f"received message = {msg}")

        northbound_full_prompt = [
            {"role": "user", "content": msg},
        ]
        northbound_message = self._generate_multi_message_completion(northbound_full_prompt)
        
        southbound_full_prompt = [
            {"role": "user", "content": msg},
        ]
        southbound_message = self._generate_multi_message_completion(southbound_full_prompt)

        logger.info(f"{northbound_message=}")
        logger.info(f"{southbound_message=}")

        if northbound_message != "none":
            await self._publish(
                queue_name=self.settings.northbound_publish_queue,
                message=northbound_message,
            )
        if southbound_message != "none":
            await self._publish(
                queue_name=self.settings.southbound_publish_queue,
                message=southbound_message,
            )
        await message.ack()


    # Override this function in your subclass, the default behavior here is to confirm the system is up and running
    async def southbound_message_handler(self, message: aio_pika.IncomingMessage):
        msg = message.body.decode()
        logger.info(f"received message = {msg}")

        northbound_full_prompt = [
            {"role": "user", "content": msg},
        ]
        northbound_message = self._generate_multi_message_completion(northbound_full_prompt)
        
        southbound_full_prompt = [
            {"role": "user", "content": msg},
        ]
        southbound_message = self._generate_multi_message_completion(southbound_full_prompt)

        logger.info(f"{northbound_message=}")
        logger.info(f"{southbound_message=}")

        if northbound_message != "none":
            await self._publish(
                queue_name=self.settings.northbound_publish_queue,
                message=northbound_message,
            )
        if southbound_message != "none":
            await self._publish(
                queue_name=self.settings.southbound_publish_queue,
                message=southbound_message,
            )
        await message.ack()


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
        nb_queue = await self.channel.declare_queue(self.settings.northbound_subscribe_queue, durable=True)
        sb_queue = await self.channel.declare_queue(self.settings.southbound_subscribe_queue, durable=True)

        await nb_queue.consume(self.northbound_message_handler)
        await sb_queue.consume(self.southbound_message_handler)

    def _generate_completion(self, conversation):
        openai.api_key = self.settings.openai_api_key
        messages = [
            {"role": "user", "content": conversation}
        ]
        completion = openai.ChatCompletion.create(
            model=self.settings.model,
            messages=messages,
            temperature=0.25,
        )
        return completion.choices[0].message["content"]
    
    def _generate_multi_message_completion(self, conversation):
        openai.api_key = self.settings.openai_api_key

        completion = openai.ChatCompletion.create(
            model=self.settings.model,
            messages=conversation,
            temperature=0.25,
        )
        return completion.choices[0].message["content"]


    async def _publish(self, queue_name, message):

        exchange = await create_exchange(
            connection=self.connection,
            queue_name=queue_name,
        )
        message_body = aio_pika.Message(
            body=message.encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await exchange.publish(
            message_body,
            routing_key=queue_name,
        )


    async def _run_layer(self):
        logger.info(f"Running {self.settings.role_name}")
        await self._connect()
        await self._subscribe()
        logger.info(f"{self.settings.role_name} Subscribed to {self.settings.northbound_subscribe_queue} and {self.settings.southbound_subscribe_queue}")


    def run(self):
        self.loop.create_task(self._run_layer())
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()


# def closest_match(input_str: str, options: List[str]):
#     scores = [fuzz.ratio(input_str, option) for option in options]
#     return options[scores.index(max(scores))]

