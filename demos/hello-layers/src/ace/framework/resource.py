import logging
import time
import json
import pika
from abc import ABC, abstractmethod

from ace import constants
from ace.settings import Settings
from ace.api_endpoint import ApiEndpoint
from ace.amqp.connection import get_connection

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Set the logger for 'pika' separately.
logging.getLogger('pika').setLevel(logging.INFO)


class Resource(ABC):
    def __init__(self):
        self.api_endpoint = ApiEndpoint(self.api_callbacks)
        self.connection = None
        self.channel = None

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
        if (orientation == 'northbound' and idx == 0) or (orientation == 'southbound' and idx == len(self.settings.layers) - 1):
            return False
        return True

    def build_all_layer_queue_names(self):
        queue_names = []
        for orientation in constants.LAYER_ORIENTATIONS:
            for idx, layer in enumerate(self.settings.layers):
                if self.is_existant_layer_queue(orientation, idx):
                    queue_names.append(self.build_queue_name(orientation, layer))
        return queue_names

    def try_queue_subscribe(self, queue_name, callback):
        while True:
            logger.debug(f"Trying to subscribe to queue: {queue_name}...")
            try:
                self.channel.queue_declare(queue=queue_name, passive=True)
                self.channel.basic_consume(queue=queue_name, on_message_callback=callback)
                logger.info(f"Subscribed to queue: {queue_name}")
                return
            except pika.exceptions.ChannelClosedByBroker:
                logger.warning(f"Queue '{queue_name}' does not exist. Trying again in 5 seconds.")
                time.sleep(5)
