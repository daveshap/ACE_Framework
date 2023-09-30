from typing import Optional
import logging
import json
import pika
from abc import abstractmethod

from ace.settings import Settings
from ace.framework.resource import Resource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LayerSettings(Settings):
    primary_directive: str
    mode: str = 'OpenAI'
    model: str = 'gpt-3.5-turbo'
    ai_retry_count: int = 3
    northern_layer: Optional[str] = None
    southern_layer: Optional[str] = None


class Layer(Resource):

    def start_resource(self):
        super().start_resource()
        self.set_adjacent_layers()
        self.register_busses()

    def stop_resource(self):
        super().stop_resource()
        self.deregister_busses()

    def set_adjacent_layers(self):
        try:
            layer_index = self.settings.layers.index(self.settings.name)
            if layer_index > 0:
                self.settings.northern_layer = self.settings.layers[layer_index - 1]
            if layer_index < len(self.settings.layers) - 1:
                self.settings.southern_layer = self.settings.layers[layer_index + 1]
        except ValueError:
            message = f"Invalid layer name: {self.settings.name}"
            logger.error(message)
            raise ValueError(message)

    def register_busses(self):
        logger.debug("Registering busses...")
        self.subscribe_busses()
        logger.debug("Registered busses...")

    def deregister_busses(self):
        logger.debug("Deregistering busses...")
        self.unsubscribe_busses()
        logger.debug("Deregistered busses...")

    def publish_message(self, exchange, message, delivery_mode=2):
        self.channel.basic_publish(exchange=exchange,
                                   routing_key="",
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=delivery_mode,
                                   ))

    def build_message(self, message=None, message_type='data'):
        message = message or {}
        message['type'] = message_type
        return json.dumps(message).encode()

    def build_queue_name(self, direction):
        queue = None
        if direction == 'northbound' and self.settings.northern_layer:
            queue = f"northbound.{self.settings.northern_layer}"
        elif direction == 'southbound' and self.settings.southern_layer:
            queue = f"southbound.{self.settings.southern_layer}"
        return queue

    def build_exchange_name(self, direction):
        exchange = None
        queue = self.build_queue_name(direction)
        if queue:
            exchange = f"exchange.{queue}"
        return exchange

    def send_message(self, direction, message, delivery_mode=2):
        exchange = self.build_exchange_name(direction)
        if exchange:
            self.publish_message(self, exchange, message)

    def ping(self, direction):
        message = self.build_message(message_type='ping')
        self.send_message(self, direction, message)

    def post(self):
        self.ping('northbound')
        self.ping('southbound')

    @abstractmethod
    def northbound_message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        # logger.info(f"I'm the [{self.labeled_name}] and I've received a [Northbound] message, here it is: {body.decode()}")
        # # For now just forward the message northward
        # time.sleep(1)
        # message = f"hello from {self.labeled_name}...".encode()
        #
        # channel.basic_publish(exchange=self.settings.northbound_publish_queue, routing_key='', body=message)
        # channel.basic_ack(delivery_tag=method.delivery_tag)
        pass

    @abstractmethod
    def southbound_message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        # logger.info(f"I'm the [{self.labeled_name}] and I've received a [Southbound] message, here it is: {body.decode()}")
        # # For now just forward the message southward
        # time.sleep(1)
        # message = f"hello from {self.labeled_name}...".encode()
        # channel.basic_publish(exchange=self.settings.southbound_publish_queue, routing_key='', body=message)
        # channel.basic_ack(delivery_tag=method.delivery_tag)
        pass

    def subscribe_busses(self):
        logger.debug(f"{self.labeled_name} subscribing to busses...")
        self.channel.basic_consume(queue=self.build_queue_name('northbound'), on_message_callback=self.northbound_message_handler)
        self.channel.basic_consume(queue=self.build_queue_name('southbound'), on_message_callback=self.southbound_message_handler)
        logger.info(f"{self.labeled_name} Subscribed to {self.settings.northbound_subscribe_queue} and {self.settings.southbound_subscribe_queue}")

    def unsubscribe_busses(self):
        northbound_queue = self.build_queue_name('northbound')
        southbound_queue = self.build_queue_name('southbound')
        logger.debug(f"{self.labeled_name} unsubscribing from busses...")
        self.channel.basic_cancel(northbound_queue)
        self.channel.basic_cancel(southbound_queue)
        logger.info(f"{self.labeled_name} Unsubscribed from {northbound_queue} and {southbound_queue}")
