import logging

from ace.settings import Settings
from ace.amqp.exchange import setup_exchange, teardown_exchange
from ace.framework.resource import Resource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BussesSettings(Settings):
    pass


class Busses(Resource):

    @property
    def settings(self):
        return BussesSettings(
            name="busses",
            label="Busses",
        )

    def start_resource(self):
        super().start_resource()
        self.create_security_queues()
        self.create_exchanges()

    def stop_resource(self):
        self.destroy_exchanges()
        self.destroy_security_queues()
        super().stop_resource()

    def create_exchanges(self):
        logger.debug(f"{self.labeled_name} creating exchanges...")
        for idx, queue_name in enumerate(self.settings.layers):
            self.create_exchange_by_index(idx, queue_name)
        logger.debug(f"{self.labeled_name} queues created")

    def create_exchange_by_index(self, idx, queue_name):
        if idx > 0:
            self.create_exchange(f"northbound.{queue_name}")
        if idx < len(self.settings.layers) - 1:
            self.create_exchange(f"southbound.{queue_name}")

    def create_exchange(self, queue_name):
        setup_exchange(
            settings=self.settings,
            connection=self.connection,
            queue_name=queue_name,
        )
        logger.info(f" Created exchange for {queue_name} for resource {self.labeled_name}")

    def destroy_exchanges(self):
        logger.debug(f"{self.labeled_name} destroying exchanges...")
        for idx, queue_name in enumerate(self.settings.layers):
            self.destroy_exchange_by_index(idx, queue_name)
        logger.debug(f"{self.labeled_name} exchanges destroyed")

    def destroy_exchange_by_index(self, idx, queue_name):
        if idx > 0:
            self.destroy_exchange(f"northbound.{queue_name}")
        if idx < len(self.settings.layers) - 1:
            self.destroy_exchange(f"southbound.{queue_name}")

    def destroy_exchange(self, queue_name):
        teardown_exchange(
            settings=self.settings,
            connection=self.connection,
            queue_name=queue_name,
        )
        logger.info(f" Destroyed exchange for {queue_name} for resource {self.labeled_name}")

    def create_security_queues(self):
        channel = self.connection.channel()
        for layer in self.settings.layers:
            queue_name = f"security.{layer}"
            channel.declare_queue(queue_name, durable=True)

    def destroy_security_queues(self):
        channel = self.connection.channel()
        for layer in self.settings.layers:
            queue_name = f"security.{layer}"
            channel.queue_delete(queue_name)
