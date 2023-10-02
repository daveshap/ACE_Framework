from base.base_layer import BaseLayer
import aio_pika
import logging
from settings import settings
from base.amqp.exchange import create_exchange
from identity import primary_directive


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Layer4Executive(BaseLayer):
    def get_primary_directive(self):
        return primary_directive


if __name__ == "__main__":
    layer = Layer4Executive(settings)
    layer.run()
