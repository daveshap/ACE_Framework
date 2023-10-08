from base.base_layer import BaseLayer
import logging
from settings import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Layer4Executive(BaseLayer):
    pass

if __name__ == "__main__":
    layer = Layer4Executive(settings)
    layer.run()
