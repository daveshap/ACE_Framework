import yaml
import aio_pika
from abc import ABC, abstractmethod

from ace.settings import Settings
from ace.framework.resource import Resource
import openai

class LayerSettings(Settings):
    mode: str = 'OpenAI'
    model: str = 'gpt-3.5-turbo'
    ai_retry_count: int = 3


class Layer(Resource):

    def post_start(self):
        self.run_layer()

    async def post_connect(self):
        self.set_adjacent_layers()
        self.set_identity()
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
            self.log.error(message)
            raise ValueError(message)

    async def register_busses(self):
        self.log.debug("Registering busses...")
        await self.subscribe_adjacent_layers()
        # TODO: Need this?
        # await self.subscribe_system_integrity_queue()
        self.log.debug("Registered busses...")

    async def deregister_busses(self):
        self.log.debug("Deregistering busses...")
        await self.unsubscribe_adjacent_layers()
        # TODO: Need this?
        # await self.unsubscribe_system_integrity_queue()
        self.log.debug("Deregistered busses...")

    @abstractmethod
    def set_identity(self):
        pass

    @abstractmethod
    def process_layer_messages(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        pass

    def run_layer(self):
        while True:
            control_messages, data_messages = None, None
            if self.northern_layer:
                control_messages = self.get_messages_from_consumer_local_queue('control')
            if self.southern_layer:
                data_messages = self.get_messages_from_consumer_local_queue('data')
            request_messages = self.get_messages_from_consumer_local_queue('request')
            response_messages = self.get_messages_from_consumer_local_queue('response')
            telemetry_messages = self.get_messages_from_consumer_local_queue('telemetry')
            messages_northbound, messages_southbound = self.process_layer_messages(control_messages, data_messages, request_messages, response_messages, telemetry_messages)
            if messages_northbound:
                for m in messages_northbound:
                    message = self.build_message(self.northern_layer, message=m, message_type=m['type'])
                    self.push_exchange_message_to_publisher_local_queue(f"northbound.{self.northern_layer}", message)
            if messages_southbound:
                for m in messages_southbound:
                    message = self.build_message(self.southern_layer, message=m, message_type=m['type'])
                    self.push_exchange_message_to_publisher_local_queue(f"southbound.{self.southern_layer}", message)

    async def send_message(self, direction, layer, message, delivery_mode=2):
        queue_name = self.build_queue_name(direction, layer)
        if queue_name:
            exchange = self.build_exchange_name(queue_name)
            await self.publish_message(exchange, message)

    def is_ping(self, data):
        return data['type'] == 'ping'

    def is_pong(self, data):
        return data['type'] == 'pong'

    async def ping(self, direction, layer):
        self.log.info(f"Sending PING: {self.labeled_name} ->  {self.build_queue_name(direction, layer)}")
        message = self.build_message(layer, message_type='ping')
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
            message = self.build_message(layer, message_type='pong')
            await self.send_message(response_direction, layer, message)

    async def post(self):
        if self.northern_layer:
            await self.ping('northbound', self.northern_layer)
        if self.southern_layer:
            await self.ping('southbound', self.southern_layer)

    async def route_message(self, direction, message):
        try:
            data = yaml.safe_load(message.body.decode())
        except yaml.YAMLError as e:
            self.log.error(f"[{self.labeled_name}] could not parse [{direction}] message: {e}")
            return
        data['direction'] = direction
        if self.is_pong(data):
            self.log.info(f"[{self.labeled_name}] received a [pong] message from layer: {data['resource']}")
            return
        elif self.is_ping(data):
            self.log.info(f"[{self.labeled_name}] received a [ping] message from layer: {data['resource']}, bus direction: {direction}")
            return await self.handle_ping(direction, data['resource'])
        self.push_message_to_consumer_local_queue(data['type'], (data, message))

    async def northbound_message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            await self.route_message('northbound', message)

    async def southbound_message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            await self.route_message('southbound', message)

    async def system_integrity_message_handler(self, message: aio_pika.IncomingMessage):
        decoded_message = message.body.decode()
        self.log.debug(f"[{self.labeled_name}] received a [System Integrity] message: {message}")
        try:
            data = yaml.safe_load(decoded_message)
        except yaml.YAMLError as e:
            self.log.error(f"[{self.labeled_name}] could not parse [System Integrity] message: {e}")
            return
        if data['type'] == 'post':
            await self.post()

    async def subscribe_adjacent_layers(self):
        if self.northern_layer:
            southbound_queue = self.build_queue_name('southbound', self.settings.name)
            self.log.debug(f"{self.labeled_name} subscribing to {southbound_queue}...")
            self.consumers[southbound_queue] = await self.try_queue_subscribe(southbound_queue, self.southbound_message_handler)
        if self.southern_layer:
            northbound_queue = self.build_queue_name('northbound', self.settings.name)
            self.log.debug(f"{self.labeled_name} subscribing to {northbound_queue}...")
            self.consumers[northbound_queue] = await self.try_queue_subscribe(northbound_queue, self.northbound_message_handler)

    # TODO: Need this?
    async def subscribe_system_integrity_queue(self):
        queue_name = f"system_integrity.{self.settings.name}"
        self.log.debug(f"{self.labeled_name} subscribing to {queue_name}...")
        self.consumers[queue_name] = await self.try_queue_subscribe(queue_name, self.system_integrity_message_handler)

    async def unsubscribe_adjacent_layers(self):
        northbound_queue = self.build_queue_name('northbound', self.northern_layer)
        southbound_queue = self.build_queue_name('southbound', self.southern_layer)
        self.log.debug(f"{self.labeled_name} unsubscribing from {northbound_queue} and {southbound_queue}...")
        if self.northern_layer and northbound_queue in self.consumers:
            await self.consumers[northbound_queue].cancel()
        if self.southern_layer and southbound_queue in self.consumers:
            await self.consumers[southbound_queue].cancel()
        self.log.info(f"{self.labeled_name} unsubscribed from {northbound_queue} and {southbound_queue}")

    # TODO: Need this?
    async def unsubscribe_system_integrity_queue(self):
        queue_name = f"system_integrity.{self.settings.name}"
        self.log.debug(f"{self.labeled_name} unsubscribing from {queue_name}...")
        if queue_name in self.consumers:
            await self.consumers[queue_name].cancel()
        self.log.info(f"{self.labeled_name} unsubscribed from {queue_name}")
