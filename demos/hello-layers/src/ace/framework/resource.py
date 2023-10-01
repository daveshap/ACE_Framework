import logging
import json
import pika
from abc import ABC, abstractmethod

from ace import constants
from ace.settings import Settings
from ace.api_endpoint import ApiEndpoint
from ace.amqp.connection import get_connection

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Resource(ABC):
    def __init__(self):
        self.api_endpoint = ApiEndpoint()
        self.connection = None
        self.channel = None

    @property
    @abstractmethod
    def settings(self) -> Settings:
        pass

    @property
    def labeled_name(self):
        return f"{self.settings.name} ({self.settings.label})"

    def start_resource(self):
        logger.info("Starting resource...")
        self.setup_service()
        logger.info("Resource started")

    def stop_resource(self):
        logger.info("Shutting down resource...")
        self.shutdown_service()
        logger.info("Resource shut down")

    def setup_service(self):
        logger.debug("Setting up service...")
        self.api_endpoint.start_endpoint()
        self.connect_busses()

    def shutdown_service(self):
        logger.debug("Shutting down service...")
        self.disconnect_busses()
        self.api_endpoint.stop_endpoint()

    def connect_busses(self):
        logger.debug(f"{self.labeled_name} connecting to busses...")
        self.connection = get_connection(self.settings)
        self.channel = self.connection.channel()
        logger.info(f"{self.labeled_name} busses connection established...")

    def disconnect_busses(self):
        logger.debug(f"{self.labeled_name} disconnecting from busses...")
        self.channel.close()
        self.connection.close()
        logger.info(f"{self.labeled_name} busses connection closed...")

    def build_message(self, message=None, message_type='data'):
        message = message or {}
        message['type'] = message_type
        return json.dumps(message).encode()

    def publish_message(self, exchange, message, delivery_mode=2):
        self.channel.basic_publish(exchange=exchange,
                                   routing_key="",
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=delivery_mode,
                                   ))

    def is_existant_layer_queue(self, orientation, idx):
        return (orientation != 'northbound' and idx != 0) and (orientation != 'southbound' and idx != len(self.settings.layers) - 1)

    def build_all_layer_queue_names(self):
        queue_names = []
        for orientation in constants.LAYER_ORIENTATIONS:
            for idx, layer in enumerate(self.settings.layers):
                if self.is_existant_layer_queue(orientation, idx):
                    queue_names.append(self.build_queue_name(orientation, layer))
        return queue_names
