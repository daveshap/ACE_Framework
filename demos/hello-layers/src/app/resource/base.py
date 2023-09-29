import logging
import pika
from abc import ABC, abstractmethod
from settings import Settings
from amqp.connection import get_connection

from resource.api_endpoint import ApiEndpoint

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Resource(ABC):
    def __init__(self, settings: Settings, api_endpoint_port=3000):
        self.api_endpoint = ApiEndpoint(api_endpoint_port)
        self.settings = settings
        self.connection = None
        self.channel = None

    def start_resource(self):
        logger.info("Starting resource...")
        self.setup_service()
        self.register_busses()
        logger.info("Resource started")

    def stop_resource(self):
        logger.info("Shutting down resource...")
        self.shutdown_service()
        self.deregister_busses()
        logger.info("Resource shut down")

    def setup_service(self):
        logger.debug("Setting up service...")
        self.api_endpoint.start_endpoint()

    def shutdown_service(self):
        logger.debug("Shutting down service...")
        self.api_endpoint.stop_endpoint()

    def register_busses(self):
        logger.debug("Registering busses...")
        self.connect_busses()
        self.subscribe_busses()
        logger.debug("Registered busses...")

    def deregister_busses(self):
        logger.debug("Deregistering busses...")
        pass  # Stub

    @abstractmethod
    def northbound_message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        # logger.info(f"I'm the [{self.settings.role_name}] and I've received a [Northbound] message, here it is: {body.decode()}")
        # # For now just forward the message northward
        # time.sleep(1)
        # message = f"hello from {self.settings.role_name}...".encode()
        #
        # channel.basic_publish(exchange=self.settings.northbound_publish_queue, routing_key='', body=message)
        # channel.basic_ack(delivery_tag=method.delivery_tag)
        pass

    @abstractmethod
    def southbound_message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        # logger.info(f"I'm the [{self.settings.role_name}] and I've received a [Southbound] message, here it is: {body.decode()}")
        # # For now just forward the message southward
        # time.sleep(1)
        # message = f"hello from {self.settings.role_name}...".encode()
        # channel.basic_publish(exchange=self.settings.southbound_publish_queue, routing_key='', body=message)
        # channel.basic_ack(delivery_tag=method.delivery_tag)
        pass

    def connect_busses(self):
        logger.debug(f"{self.settings.role_name} connecting to busses...")
        self.connection = get_connection()
        self.channel = self.connection.channel()
        logger.info(f"{self.settings.role_name} busses connection established...")

    def subscribe_busses(self):
        logger.debug(f"{self.settings.role_name} subscrbing to busses...")
        nb_queue = self.channel.declare_queue(self.settings.northbound_subscribe_queue, durable=True)
        sb_queue = self.channel.declare_queue(self.settings.southbound_subscribe_queue, durable=True)
        logger.info(f"{self.settings.role_name} Subscribed to {self.settings.northbound_subscribe_queue} and {self.settings.southbound_subscribe_queue}")

        nb_queue.consume(self.northbound_message_handler)
        sb_queue.consume(self.southbound_message_handler)
