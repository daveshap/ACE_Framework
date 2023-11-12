from base.base_layer import BaseLayer
import logging
from settings import settings
import re


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Layer3Agent(BaseLayer):

    # express limitations and capabilities.
    def _extract_status(self, input_text):
        match = re.search(r'\[Status\]\n(complete|incomplete|error)', input_text)
        
        if match:
            return match.group(1).strip().lower()
        else:
            return 'error'


if __name__ == "__main__":
    layer = Layer3Agent(settings)
    layer.run()
