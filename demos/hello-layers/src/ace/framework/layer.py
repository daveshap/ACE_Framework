import logging
import json
import aio_pika
from abc import abstractmethod

from ace import constants
from ace.settings import Settings
from ace.framework.resource import Resource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LayerSettings(Settings):
    primary_directive: str
    mode: str = 'OpenAI'
    model: str = 'gpt-3.5-turbo'
    ai_retry_count: int = 3


class Layer(Resource):

    async def post_connect(self):
        self.set_adjacent_layers()
        await self.register_busses()

    async def pre_disconnect(self):
        await self.deregister_busses()

    def set_adjacent_layers(self):
        self.northern_layer = None
        self.southern_layer = None
        try:
            layer_index = self.settings.layers.index(self.settings.name)
            if layer_index > 0:
                self.northern_layer = self.settings.layers[layer_index - 1]
            if layer_index < len(self.settings.layers) - 1:
                self.southern_layer = self.settings.layers[layer_index + 1]
        except ValueError:
            message = f"Invalid layer name: {self.settings.name}"
            logger.error(message)
            raise ValueError(message)

    async def register_busses(self):
        logger.debug("Registering busses...")
        await self.subscribe_adjacent_layers()
        # TODO: Need this?
        # await self.subscribe_security_queue()
        logger.debug("Registered busses...")

    async def deregister_busses(self):
        logger.debug("Deregistering busses...")
        await self.unsubscribe_adjacent_layers()
        # TODO: Need this?
        # await self.unsubscribe_security_queue()
        logger.debug("Deregistered busses...")

    async def send_message(self, direction, layer, message, delivery_mode=2):
        exchange = self.build_exchange_name(direction, layer)
        if exchange:
            await self.publish_message(exchange, message)

    def is_ping(self, data):
        return data['type'] == 'ping'

    def is_pong(self, data):
        return data['type'] == 'pong'

    async def ping(self, direction, layer):
        message = self.build_message(message_type='ping')
        await self.send_message(self, direction, layer, message)

    async def handle_ping(self, direction, layer):
        response_direction = None
        layer = None
        if direction == 'northbound':
            response_direction = 'southbound'
            layer = self.southern_layer
        elif direction == 'southbound':
            response_direction = 'northbound'
            layer = self.northern_layer
        if response_direction and layer:
            message = self.build_message(message_type='pong')
            await self.send_message(response_direction, layer, message)

    async def post(self):
        if self.northern_layer:
            await self.ping('northbound', self.northern_layer)
        if self.southern_layer:
            await self.ping('southbound', self.southern_layer)

    async def route_message(self, direction, message):
        try:
            data = json.loads(message.body.decode())
        except json.JSONDecodeError as e:
            logger.error(f"[{self.labeled_name}] could not parse [{direction}] message: {e}")
            return
        if self.is_pong(data):
            logger.info(f"[{self.labeled_name}] received a [pong] message from layer: {data['resource']}")
            return
        elif self.is_ping(data):
            logger.info(f"[{self.labeled_name}] received a [ping] message from layer: {data['resource']}, bus direction: {direction}")
            return await self.handle_ping(direction, data['resource'])
        self.push_message_to_consumer_local_queue(data['type'], data, message)

    async def northbound_message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            await self.route_message('northbound', message)

    async def southbound_message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            await self.route_message('southbound', message)

    async def security_message_handler(self, message: aio_pika.IncomingMessage):
        message = message.body.decode()
        logger.debug(f"[{self.labeled_name}] received a [Security] message: {message}")
        try:
            data = json.loads(message)
        except json.JSONDecodeError as e:
            logger.error(f"[{self.labeled_name}] could not parse [Security] message: {e}")
            return
        if data['type'] == 'post':
            await self.post()

    async def subscribe_adjacent_layers(self):
        northbound_queue = self.build_queue_name('northbound', self.northern_layer)
        southbound_queue = self.build_queue_name('southbound', self.southern_layer)
        logger.debug(f"{self.labeled_name} subscribing to {northbound_queue} and {southbound_queue}...")
        if self.northern_layer:
            self.consumers[northbound_queue] = await self.try_queue_subscribe(northbound_queue, self.northbound_message_handler)
        if self.southern_layer:
            self.consumers[southbound_queue] = await self.try_queue_subscribe(southbound_queue, self.southbound_message_handler)

    # TODO: Need this?
    async def subscribe_security_queue(self):
        queue_name = f"security.{self.settings.name}"
        logger.debug(f"{self.labeled_name} subscribing to {queue_name}...")
        self.consumers[queue_name] = await self.try_queue_subscribe(queue_name, self.security_message_handler)

    async def unsubscribe_adjacent_layers(self):
        northbound_queue = self.build_queue_name('northbound', self.northern_layer)
        southbound_queue = self.build_queue_name('southbound', self.southern_layer)
        logger.debug(f"{self.labeled_name} unsubscribing from {northbound_queue} and {southbound_queue}...")
        if self.northern_layer and northbound_queue in self.consumers:
            await self.consumers[northbound_queue].cancel()
        if self.southern_layer and southbound_queue in self.consumers:
            await self.consumers[southbound_queue].cancel()
        logger.info(f"{self.labeled_name} unsubscribed from {northbound_queue} and {southbound_queue}")

    # TODO: Need this?
    async def unsubscribe_security_queue(self):
        queue_name = f"security.{self.settings.name}"
        logger.debug(f"{self.labeled_name} unsubscribing from {queue_name}...")
        if queue_name in self.consumers:
            await self.consumers[queue_name].cancel()
        logger.info(f"{self.labeled_name} unsubscribed from {queue_name}")
