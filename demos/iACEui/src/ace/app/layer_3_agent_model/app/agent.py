from base.base_layer import BaseLayer
import aio_pika
import logging
from settings import settings
from base.amqp.exchange import create_exchange

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Layer3Agent(BaseLayer):
    pass


if __name__ == "__main__":
    layer = Layer3Agent(settings)
    layer.run()
