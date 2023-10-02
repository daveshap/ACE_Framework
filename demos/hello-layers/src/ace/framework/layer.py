import logging
import json
import pika
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

    def start_resource(self):
        super().start_resource()
        self.set_adjacent_layers()
        self.register_busses()

    def stop_resource(self):
        self.deregister_busses()
        super().stop_resource()

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

    def register_busses(self):
        logger.debug("Registering busses...")
        self.subscribe_adjacent_layers()
        self.subscribe_security_queue()
        logger.debug("Registered busses...")

    def deregister_busses(self):
        logger.debug("Deregistering busses...")
        self.unsubscribe_adjacent_layers()
        self.unsubscribe_security_queue()
        logger.debug("Deregistered busses...")

    def build_queue_name(self, direction, layer):
        queue = None
        if layer and direction in constants.LAYER_ORIENTATIONS:
            queue = f"{direction}.{layer}"
        return queue

    def build_exchange_name(self, direction, layer):
        exchange = None
        queue = self.build_queue_name(direction, layer)
        if queue:
            exchange = f"exchange.{queue}"
        return exchange

    def send_message(self, direction, layer, message, delivery_mode=2):
        exchange = self.build_exchange_name(direction, layer)
        if exchange:
            self.publish_message(self, exchange, message)

    def ping(self, direction, layer):
        message = self.build_message(message_type='ping')
        self.send_message(self, direction, layer, message)

    def post(self):
        self.ping('northbound', self.northern_layer)
        self.ping('southbound', self.southern_layer)

    def route_message(self, direction, body):
        try:
            data = json.loads(body.decode())
        except json.JSONDecodeError as e:
            logger.error(f"[{self.labeled_name}] could not parse [{direction}] message: {e}")
            return
        try:
            handler = getattr(self, f"handle_message_{data['type']}")
        except AttributeError as e:
            logger.error(f"[{self.labeled_name}] missing handler type '{data['type']}' for [{direction}] message: {e}")
            return
        handler(data)

    def northbound_message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        self.route_message('Northbound', body)
        # logger.info(f"I'm the [{self.labeled_name}] and I've received a [Northbound] message, here it is: {body.decode()}")
        # # For now just forward the message northward
        # time.sleep(1)
        # message = f"hello from {self.labeled_name}...".encode()
        #
        # channel.basic_publish(exchange=self.settings.northbound_publish_queue, routing_key='', body=message)
        # channel.basic_ack(delivery_tag=method.delivery_tag)

    def southbound_message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        self.route_message('Southbound', body)
        # logger.info(f"I'm the [{self.labeled_name}] and I've received a [Southbound] message, here it is: {body.decode()}")
        # # For now just forward the message southward
        # time.sleep(1)
        # message = f"hello from {self.labeled_name}...".encode()
        # channel.basic_publish(exchange=self.settings.southbound_publish_queue, routing_key='', body=message)
        # channel.basic_ack(delivery_tag=method.delivery_tag)

    @abstractmethod
    def handle_message_control(self, data):
        pass

    @abstractmethod
    def handle_message_data(self, data):
        pass

    def security_message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        message = body.decode()
        logger.debug(f"[{self.labeled_name}] received a [Security] message: {message}")
        try:
            data = json.loads(message)
        except json.JSONDecodeError as e:
            logger.error(f"[{self.labeled_name}] could not parse [Security] message: {e}")
            return
        if data['type'] == 'post':
            self.post()

    def subscribe_adjacent_layers(self):
        northbound_queue = self.build_queue_name('northbound', self.northern_layer)
        southbound_queue = self.build_queue_name('southbound', self.southern_layer)
        logger.debug(f"{self.labeled_name} subscribing to {northbound_queue} and {southbound_queue}...")
        if self.northern_layer:
            self.try_queue_subscribe(northbound_queue, self.northbound_message_handler)
        if self.southern_layer:
            self.try_queue_subscribe(southbound_queue, self.southbound_message_handler)

    def subscribe_security_queue(self):
        queue_name = f"security.{self.settings.name}"
        logger.debug(f"{self.labeled_name} subscribing to {queue_name}...")
        self.try_queue_subscribe(queue_name, self.security_message_handler)

    def unsubscribe_adjacent_layers(self):
        northbound_queue = self.build_queue_name('northbound', self.northern_layer)
        southbound_queue = self.build_queue_name('southbound', self.southern_layer)
        logger.debug(f"{self.labeled_name} unsubscribing from {northbound_queue} and {southbound_queue}...")
        if self.northern_layer:
            self.channel.basic_cancel(northbound_queue)
        if self.southern_layer:
            self.channel.basic_cancel(southbound_queue)
        logger.info(f"{self.labeled_name} unsubscribed from {northbound_queue} and {southbound_queue}")

    def unsubscribe_security_queue(self):
        queue_name = f"security.{self.settings.name}"
        logger.debug(f"{self.labeled_name} unsubscribing from {queue_name}...")
        self.channel.basic_cancel(queue_name)
        logger.info(f"{self.labeled_name} unsubscribed from {queue_name}")
