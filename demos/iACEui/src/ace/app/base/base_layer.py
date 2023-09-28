import asyncio
import logging
import aio_pika
from abc import ABC
from base.settings import Settings
from base.amqp.connection import get_connection
from base.amqp.exchange import create_exchange
import time
import openai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseLayer(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings
        self.loop = asyncio.get_event_loop()
        self.connection = None
        self.channel = None

        self.primary_directive_messages=[
            {"role": "system", "content": GLOBAL_SYSTEM_ROLE},
            {"role": "system", "content": self.settings.primary_directive},
            {"role": "user", "content": "Give me a brief summary about who or what you are."}
        ]


        logger.info(f"setting {self.settings.role_name} Layer's mission")
        
        openai.api_key = settings.openai_api_key

        chat_completion = openai.ChatCompletion.create(
            model=self.settings.model,
            messages=self.primary_directive_messages,
            temperature=0.25,
        )
        logger.info(chat_completion)


    # Override this function in your subclass, the default behavior here is to confirm the system is up and running
    async def northbound_message_handler(self, message: aio_pika.IncomingMessage):
        logger.info(f"I'm the [{self.settings.role_name}] and I've received a [Northbound] message, here it is: {message.body.decode()}")

        exchange = await create_exchange(
            connection=self.connection,
            queue_name=self.settings.northbound_publish_queue,
        )
        # For now just forward the message southward
        time.sleep(1)
        message_body = aio_pika.Message(
            body=f"hello from {self.settings.role_name}...".encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await exchange.publish(
            message_body,
            routing_key=self.settings.northbound_publish_queue,
        )
        
        await message.ack()  # acknowledge the message


    # Override this function in your subclass, the default behavior here is to confirm the system is up and running
    async def southbound_message_handler(self, message: aio_pika.IncomingMessage):
        logger.info(f"I'm the [{self.settings.role_name}] and I've received a [Southbound] message, here it is: {message.body.decode()}")

        exchange = await create_exchange(
            connection=self.connection,
            queue_name=self.settings.southbound_publish_queue,
        )
        # For now just forward the message southward
        time.sleep(1)
        message_body = aio_pika.Message(
            body=f"hello from {self.settings.role_name}...".encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        await exchange.publish(
            message_body,
            routing_key=self.settings.southbound_publish_queue,
        )
        
        await message.ack()  # acknowledge the message

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


GLOBAL_SYSTEM_ROLE = """
# ACE Framework System Prompt

## Overview:
The **ACE (Autonomous Cognitive Entity) Framework** is a blueprint for creating self-guiding and ethically-informed autonomous entities.

## Approach:
- **Cognition-First**: Prioritizes deep cognitive processes over simple reactive behaviors. 

## Layers:
1. **Aspirational Layer**: Ethical compass, aligns agent's values with predefined principles.
2. **Global Strategy Layer**: Sets overarching goals and strategic plans based on context.
3. **Agent Model Layer**: Creates a self-awareness model detailing capabilities and limitations.
4. **Executive Function Layer**: Converts strategies into detailed plans; allocates resources.
5. **Cognitive Control Layer**: Dynamically selects and switches tasks based on environment and internal states.
6. **Task Prosecution Layer**: Executes tasks, interacts with the external environment.

## Communication:
- **Northbound Bus**: Carries data upwards (sensory and internal states).
- **Southbound Bus**: Sends directives and instructions downward.
- **Human-Readable**: Messages are in clear, human-readable format.

## Principles:
- Inspired by models like **Maslow's Hierarchy**.
- **Top-Down Control**: Aspirational Layer is the primary guiding force.
- **Abstract-to-Concrete Design**: Top layers are conceptual; bottom layers are actionable.

## Objective:
Develop aligned AGI systems that are transparent, correctable, and beneficial by design.
"""