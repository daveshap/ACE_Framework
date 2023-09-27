import asyncio
import logging
import aio_pika
from abc import ABC
from base.settings import Settings
from base.amqp.connection import get_connection
from base.amqp.exchange import create_exchange
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseLayer(ABC):

    def __init__(self, settings: Settings):
        self.settings = settings
        self.loop = asyncio.get_event_loop()
        self.connection = None
        self.channel = None


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
        self.connection = await get_connection(loop=self.loop)
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
