from abc import ABC, abstractmethod

import os
import time
from datetime import datetime
import yaml
import asyncio
import aio_pika
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from ace import constants
from ace.settings import Settings
from ace.api_endpoint import ApiEndpoint
from ace.amqp.config_parser import ConfigParser
from ace.amqp.connection import AMQPConnectionManager
from ace.amqp.setup import AMQPSetupManager

from ace.logger import Logger


class Resource(ABC):
    def __init__(self):
        self.log = Logger(self.__class__.__name__)
        self.api_endpoint = ApiEndpoint(self.api_callbacks)
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.connection_manager = AMQPConnectionManager(self.settings)
        self.bus_loop = asyncio.new_event_loop()
        self.connection = None
        self.consumer_channel = None
        self.publisher_channel = None
        self.consumers = {}
        self.consumer_local_queues = {}
        self.publisher_local_queue = None
        self.publish_messages = False
        self.set_debug_state()

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

    async def post_connect(self):
        pass

    async def pre_disconnect(self):
        pass

    def post_start(self):
        pass

    def pre_stop(self):
        pass

    def return_status(self, up, data=None):
        data = data or {}
        data['up'] = up
        return data

    def set_debug_state(self, debug_mode=None):
        self.debug_mode = bool(os.getenv('ACE_DEBUG_MODE')) if debug_mode is None else debug_mode

    def configure_messaging(self):
        self.config_parser = ConfigParser()
        self.messaging_config = AMQPSetupManager(self.config_parser)
        self.get_resource_messaging_config()
        self.log.debug(f"{self.labeled_name} configured messaging...")

    def get_resource_messaging_config(self):
        resources = self.config_parser.get_resources()
        try:
            self.resource_config = resources[self.settings.name]
        except KeyError as e:
            message = f"{self.labeled_name} resource config not found: {e}"
            self.log.error(message)
            raise KeyError(message)

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
        self.connection = await self.connection_manager.get_connection(loop=self.bus_loop)
        self.consumer_channel = await self.connection.channel()
        self.publisher_channel = await self.connection.channel()
        self.log.info(f"{self.labeled_name} busses connection established...")

    def disconnect_busses(self):
        self.log.info(f"{self.labeled_name} disconnecting from busses...")
        self.stop_publisher_local_queue()

        async def close_connections():
            await asyncio.sleep(1)
            self.unsubscribe_messaging()
            await self.pre_disconnect()
            await self.publisher_channel.close()
            await self.consumer_channel.close()
            await self.connection.close()
            self.log.info(f"{self.labeled_name} busses connection closed...")
            self.bus_loop.stop()

        asyncio.run_coroutine_threadsafe(close_connections(), self.bus_loop)

    def start_resource(self):
        self.log.info("Starting resource...")
        self.setup_service()
        self.wait_for_local_publisher_queue()
        future = asyncio.run_coroutine_threadsafe(self.subscribe_messaging(), self.bus_loop)
        future.result()
        self.post_start()
        self.log.info("Resource started")

    def stop_resource(self):
        self.log.info("Shutting down resource...")
        self.pre_stop()
        self.shutdown_service()
        self.log.info("Resource shut down")

    def setup_service(self):
        self.log.debug("Setting up service...")
        self.api_endpoint.start_endpoint()
        self.configure_messaging()
        self.connect_busses()

    def shutdown_service(self):
        self.log.debug("Shutting down service...")
        self.disconnect_busses()
        self.api_endpoint.stop_endpoint()

    def wait_for_local_publisher_queue(self):
        # TODO: Would be nice if this was cleaner, but we need to wait on the
        # messaging thread to call post_start().
        while not self.publisher_local_queue:
            self.log.debug(f"[{self.labeled_name}] waiting for publisher local queue...")
            time.sleep(1)

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

    def stop_publisher_local_queue(self):
        self.publish_messages = False
        # Kick the queue to break the loop.
        self.push_exchange_message_to_publisher_local_queue(None, None)

    def push_pathway_message_to_publisher_local_queue(self, pathway_name, message):
        pathway = self.build_pathway_name(pathway_name)
        self.push_exchange_message_to_publisher_local_queue(pathway, message)

    def push_exchange_message_to_publisher_local_queue(self, queue_name, message):
        data = (queue_name, message)
        self.bus_loop.call_soon_threadsafe(self.publisher_local_queue.put_nowait, data)

    async def process_publisher_messages_to_exchanges(self):
        self.publisher_local_queue = asyncio.Queue()
        self.publish_messages = True
        while self.publish_messages:
            try:
                data = await self.publisher_local_queue.get()
                queue_name, message = data
                if queue_name:
                    await self.publish_message(self.build_exchange_name(queue_name), message)
            except Exception as e:
                self.log.error(f"Publishing message from local publisher queue failed: {e}", exc_info=True)
                continue

    def build_pathway_name(self, pathway_name):
        if pathway_name in self.resource_config.default_pathways:
            return f"pathway.{self.settings.name}.{pathway_name}"
        self.log.error(f"Invalid pathway name for resource {self.settings.name}: {pathway_name}")
        return None

    def build_layer_queue_name(self, direction, layer):
        queue = None
        if layer and direction in constants.LAYER_ORIENTATIONS:
            queue = f"{direction}.{layer}"
        return queue

    def build_system_integrity_queue_name(self, layer):
        return f"system_integrity.{layer}"

    def build_debug_queue_name(self, layer):
        return f"debug.{layer}"

    def build_telemetry_queue_name(self, name):
        return f"telemetry.{name}"

    def build_exchange_name(self, queue_name):
        return f"exchange.{queue_name}"

    def build_message(self, destination, message=None, message_type='data'):
        message = message or {}
        message['type'] = message_type
        message['resource'] = {
            'source': self.settings.name,
            'destination': destination,
        }
        message['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return yaml.dump(message, default_flow_style=False).encode()

    async def publish_message(self, exchange_name, message, delivery_mode=2):
        exchange = await self.try_get_exchange(exchange_name)
        message = aio_pika.Message(
            body=message,
            delivery_mode=delivery_mode
        )
        self.log.debug(f"Publishing message, exchange {exchange.name}")
        await exchange.publish(message, routing_key="")

    def is_existant_layer_queue(self, orientation, idx):
        # Queue names are [direction].[destination_layer], so there is no:
        # 1. southbound to the first layer
        # 2. northbound to the last layer
        if (orientation == 'southbound' and idx == 0) or (orientation == 'northbound' and idx == len(self.settings.layers) - 1):
            return False
        return True

    async def try_queue_subscribe(self, queue_name, callback):
        while True:
            self.log.debug(f"Trying to subscribe to queue: {queue_name}...")
            try:
                if self.consumer_channel.is_closed:
                    self.log.info("Previous channel was closed, creating new channel...")
                    self.consumer_channel = await self.connection.channel()
                queue = await self.consumer_channel.get_queue(queue_name)
                consumer_tag = await queue.consume(callback)
                self.log.info(f"Subscribed to queue: {queue_name}")
                return queue, consumer_tag
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

    async def subscribe_messaging(self):
        for queue_name, handler in self.resource_config.subscribes_to.items():
            await self.subscribe_queue(queue_name, handler)

    async def subscribe_queue(self, queue_name: str, handler: str):
        try:
            handler_method = getattr(self, handler)
        except AttributeError:
            message = f"Queue handler for queue {queue_name} not found: {handler}"
            self.log.error(message)
            raise AttributeError(message)
        self.log.debug(f"{self.labeled_name} subscribing to {queue_name}, handler: {handler}...")
        self.consumers[queue_name] = await self.try_queue_subscribe(queue_name, handler_method)

    async def unsubscribe_messaging(self):
        for queue_name, queue_config in self.consumers.items():
            queue, consumer_tag = queue_config
            await self.unsubscribe_queue(queue_name, queue, consumer_tag)

    async def unsubscribe_queue(self, queue_name: str, queue: aio_pika.Queue, consumer_tag: str):
        self.log.debug(f"{self.labeled_name} unsubscribing from {queue_name}...")
        await queue.cancel(consumer_tag)
        self.log.info(f"{self.labeled_name} unsubscribed from {queue_name}")

    async def system_integrity_message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            decoded_message = message.body.decode()
        self.log.debug(f"[{self.labeled_name}] received a [System Integrity] message: {message}")
        try:
            data = yaml.safe_load(decoded_message)
        except yaml.YAMLError as e:
            self.log.error(f"[{self.labeled_name}] could not parse [System Integrity] message: {e}", exc_info=True)
            return
        if data['type'] == 'command':
            method = data.get('method')
            kwargs = data.get('kwargs')
            await self.system_integrity_run_command(method, kwargs)

    async def system_integrity_run_command(self, method_name: str, kwargs: dict = None):
        kwargs = kwargs or {}
        self.log.debug(f"[{self.labeled_name}] received a [System Integrity] command, method: {method_name}, args: {kwargs}")
        try:
            method = getattr(self, method_name)
            method(**kwargs)
        except Exception as e:
            self.log.error(f"[{self.labeled_name}] failed [System Integrity] command: method {method_name}, error: {e}", exc_info=True)

    async def subscribe_debug_queue(self):
        queue_name = self.build_debug_queue_name(self.settings.name)
        self.log.debug(f"{self.labeled_name} subscribing to {queue_name}...")
        self.consumers[queue_name] = await self.try_queue_subscribe(queue_name, self.debug_message_handler)

    async def unsubscribe_debug_queue(self):
        queue_name = self.build_debug_queue_name(self.settings.name)
        if queue_name in self.consumers:
            queue, consumer_tag = self.consumers[queue_name]
            self.log.debug(f"{self.labeled_name} unsubscribing from {queue_name}...")
            await queue.cancel(consumer_tag)
            self.log.info(f"{self.labeled_name} unsubscribed from {queue_name}")

    async def debug_message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            decoded_message = message.body.decode()
        self.log.debug(f"[{self.labeled_name}] received a [Debug] message: {message}")
        try:
            data = yaml.safe_load(decoded_message)
        except yaml.YAMLError as e:
            self.log.error(f"[{self.labeled_name}] could not parse [Debug] message: {e}", exc_info=True)
            return
        if data['type'] == 'command':
            method = data.get('method')
            kwargs = data.get('kwargs')
            await self.debug_run_command(method, kwargs)

    async def debug_run_command(self, method_name: str, kwargs: dict = None):
        kwargs = kwargs or {}
        self.log.debug(f"[{self.labeled_name}] received a [Debug] command, method: {method_name}, args: {kwargs}")
        try:
            method = getattr(self, method_name)
            method(**kwargs)
        except Exception as e:
            self.log.error(f"[{self.labeled_name}] failed [Debug] command: method {method_name}, error: {e}", exc_info=True)

    def resource_log(self, message):
        self.log.info(f"{self.labeled_name} resource log: \n\n{message}\n\n")
        log_message = self.build_message('logging', message={'message': message}, message_type='log')
        self.push_exchange_message_to_publisher_local_queue(self.settings.resource_log_queue, log_message)

    def telemetry_subscribe_to_namespace(self, namespace):
        self.telemetry_subscribe_unsubscribe_namespace('subscribe', namespace)

    def telemetry_unsubscribe_from_namespace(self, namespace):
        self.telemetry_subscribe_unsubscribe_namespace('unsubscribe', namespace)

    def telemetry_subscribe_unsubscribe_namespace(self, message_type, namespace):
        self.log.info(f"{self.labeled_name} '{message_type}' telemetry namespace: {namespace}")
        message = self.build_message('telemetry', message={'queue': self.build_telemetry_queue_name(self.settings.name), 'namespace': namespace}, message_type=message_type)
        self.push_exchange_message_to_publisher_local_queue(self.settings.telemetry_subscribe_queue, message)
