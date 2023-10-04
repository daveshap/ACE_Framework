from abc import ABC, abstractmethod

import yaml
import asyncio
import aio_pika
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from queue import Queue

from ace import constants
from ace.settings import Settings
from ace.api_endpoint import ApiEndpoint
from ace.amqp.connection import get_connection

from ace.logger import Logger


class Resource(ABC):
    def __init__(self):
        self.log = Logger(self.__class__.__name__)
        self.api_endpoint = ApiEndpoint(self.api_callbacks)
        self.bus_loop = asyncio.new_event_loop()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.connection = None
        self.consumer_channel = None
        self.publisher_channel = None
        self.consumers = {}
        self.consumer_local_queues = {}
        self.publisher_local_queue = None

    @property
    @abstractmethod
    def settings(self) -> Settings:
        pass

    @property
    def labeled_name(self):
        return f"{self.settings.name} ({self.settings.label})"

    @property
    def api_callbacks(self):
        return {
            'status': self.status
        }

    @abstractmethod
    def status(self):
        pass

    def return_status(self, up, data=None):
        data = data or {}
        data['up'] = up
        return data

    def connect_busses(self):
        self.log.debug(f"{self.labeled_name} connecting to busses...")
        Thread(target=self.connect_busses_in_thread).start()

    def connect_busses_in_thread(self):
        asyncio.set_event_loop(self.bus_loop)
        self.bus_loop.run_until_complete(self.get_busses_connection_and_channel())
        self.bus_loop.run_until_complete(self.post_connect())
        self.bus_loop.run_until_complete(self.process_publisher_messages_to_exchanges())
        self.bus_loop.run_forever()

    async def get_busses_connection_and_channel(self):
        self.log.debug(f"{self.labeled_name} getting busses connection and channels...")
        self.connection = await get_connection(settings=self.settings, loop=self.bus_loop)
        self.consumer_channel = await self.connection.channel()
        self.publisher_channel = await self.connection.channel()
        self.log.info(f"{self.labeled_name} busses connection established...")

    def disconnect_busses(self):
        self.log.debug(f"{self.labeled_name} disconnecting from busses...")
        self.bus_loop.run_until_complete(self.pre_disconnect())
        self.bus_loop.run_until_complete(self.publisher_channel.close())
        self.bus_loop.run_until_complete(self.consumer_channel.close())
        self.bus_loop.run_until_complete(self.connection.close())
        self.bus_loop.call_soon_threadsafe(self.bus_loop.stop)
        self.log.info(f"{self.labeled_name} busses connection closed...")

    async def post_connect(self):
        pass

    def post_start(self):
        pass

    async def pre_disconnect(self):
        pass

    def start_resource(self):
        self.log.info("Starting resource...")
        self.setup_service()
        # TODO: This isn't ideal, as the other thread still needs time to start up before this should be called.
        self.post_start()
        self.log.info("Resource started")

    def stop_resource(self):
        self.log.info("Shutting down resource...")
        self.shutdown_service()
        self.log.info("Resource shut down")

    def setup_service(self):
        self.log.debug("Setting up service...")
        self.api_endpoint.start_endpoint()
        self.connect_busses()

    def shutdown_service(self):
        self.log.debug("Shutting down service...")
        self.disconnect_busses()
        self.api_endpoint.stop_endpoint()

    def get_consumer_local_queue(self, queue_name):
        if queue_name not in self.consumer_local_queues:
            self.consumer_local_queues[queue_name] = Queue()
        return self.consumer_local_queues[queue_name]

    def push_message_to_consumer_local_queue(self, queue_name, message):
        self.get_consumer_local_queue(queue_name).put(message)

    def get_messages_from_consumer_local_queue(self, queue_name):
        messages = []
        queue = self.get_consumer_local_queue(queue_name)
        while not queue.empty():
            messages.append(queue.get())
        return messages

    def push_exchange_message_to_publisher_local_queue(self, queue_name, message):
        data = (queue_name, message)
        self.bus_loop.call_soon_threadsafe(self.publisher_local_queue.put_nowait, data)

    async def process_publisher_messages_to_exchanges(self):
        self.publisher_local_queue = asyncio.Queue()
        while True:
            try:
                data = await self.publisher_local_queue.get()
                queue_name, message = data
                await self.publish_message(self.build_exchange_name(queue_name), message)
            except Exception as e:
                self.log.error(f"Publishing message from local publisher queue failed: {e}")
                continue

    def build_queue_name(self, direction, layer):
        queue = None
        if layer and direction in constants.LAYER_ORIENTATIONS:
            queue = f"{direction}.{layer}"
        return queue

    def build_exchange_name(self, queue_name):
        return f"exchange.{queue_name}"

    def build_message(self, destination, message=None, message_type='data'):
        message = message or {}
        message['type'] = message_type
        message['resource'] = {
            'source': self.settings.name,
            'destination': destination,
        }
        return yaml.dump(message, default_flow_style=False).encode()

    async def publish_message(self, exchange_name, message, delivery_mode=2):
        exchange = await self.try_get_exchange(exchange_name)
        message = aio_pika.Message(
            body=message,
            delivery_mode=delivery_mode
        )
        await exchange.publish(message, routing_key="")

    def is_existant_layer_queue(self, orientation, idx):
        # Queue names are [direction].[destination_layer], so there is no:
        # 1. southbound to the first layer
        # 2. northbound to the last layer
        if (orientation == 'southbound' and idx == 0) or (orientation == 'northbound' and idx == len(self.settings.layers) - 1):
            return False
        return True

    def build_all_layer_queue_names(self):
        queue_names = []
        for orientation in constants.LAYER_ORIENTATIONS:
            for idx, layer in enumerate(self.settings.layers):
                if self.is_existant_layer_queue(orientation, idx):
                    queue_names.append(self.build_queue_name(orientation, layer))
        return queue_names

    async def try_queue_subscribe(self, queue_name, callback):
        while True:
            self.log.debug(f"Trying to subscribe to queue: {queue_name}...")
            try:
                if self.consumer_channel.is_closed:
                    self.log.info("Previous channel was closed, creating new channel...")
                    self.consumer_channel = await self.connection.channel()
                queue = await self.consumer_channel.get_queue(queue_name)
                await queue.consume(callback)
                self.log.info(f"Subscribed to queue: {queue_name}")
                return
            except (aio_pika.exceptions.ChannelClosed, aio_pika.exceptions.ChannelClosed) as e:
                self.log.warning(f"Error occurred: {str(e)}. Trying again in {constants.QUEUE_SUBSCRIBE_RETRY_SECONDS} seconds.")
                await asyncio.sleep(constants.QUEUE_SUBSCRIBE_RETRY_SECONDS)

    async def try_get_exchange(self, exchange_name):
        while True:
            self.log.debug(f"Trying to get exchange: {exchange_name}...")
            try:
                if self.publisher_channel.is_closed:
                    self.log.info("Previous channel was closed, creating new channel...")
                    self.publisher_channel = await self.connection.channel()
                exchange = await self.publisher_channel.get_exchange(exchange_name)
                return exchange
            except (aio_pika.exceptions.ChannelClosed, aio_pika.exceptions.ChannelClosed) as e:
                self.log.warning(f"Error occurred: {str(e)}. Trying again in {constants.QUEUE_SUBSCRIBE_RETRY_SECONDS} seconds.")
                await asyncio.sleep(constants.QUEUE_SUBSCRIBE_RETRY_SECONDS)
