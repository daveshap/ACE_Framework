from base.base_layer import BaseLayer
import aio_pika
import logging
from settings import settings
from base.amqp.exchange import create_exchange
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Layer1Aspirant(BaseLayer):
    pass

if __name__ == "__main__":
    layer = Layer1Aspirant(settings)
    layer.run()
