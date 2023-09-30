import logging

from ace.settings import Settings
from ace.amqp.exchange import make_exchange
from ace.framework.resource import Resource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BussesSettings(Settings):
    pass


class Busses(Resource):

    @property
    def settings(self):
        return BussesSettings()

    def create_exchanges(self):
        logger.debug(f"{self.labeled_name} creating queues...")
        for idx, queue_name in enumerate(self.settings.layers):
            self.create_exchange_by_index(idx, queue_name)
        logger.debug(f"{self.labeled_name} queues created")

    def create_exchange_by_index(self, idx, queue_name):
        if idx > 0:
            self.create_exchange(f"northbound.{queue_name}")
        if idx < len(self.settings.layers) - 1:
            self.create_exchange(f"southbound.{queue_name}")

    def create_exchange(self, queue_name):
        make_exchange(
            settings=self.settings,
            connection=self.connection,
            queue_name=queue_name,
        )
        logger.info(f" Created queue {queue_name} for resource {self.labeled_name}")
