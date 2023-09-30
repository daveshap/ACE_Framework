import logging
from abc import ABC, abstractmethod
from settings import Settings

from amqp.connection import get_connection
from resource.api_endpoint import ApiEndpoint

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
        self.connection = get_connection()
        self.channel = self.connection.channel()
        logger.info(f"{self.labeled_name} busses connection established...")

    def disconnect_busses(self):
        logger.debug(f"{self.labeled_name} disconnecting from busses...")
        self.channel.close()
        self.connection.close()
        logger.info(f"{self.labeled_name} busses connection closed...")
