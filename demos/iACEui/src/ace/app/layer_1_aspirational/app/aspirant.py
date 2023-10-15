from base.base_layer import BaseLayer
import logging
from settings import settings
import re


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Layer1Aspirant(BaseLayer):

    def _extract_judgement(self, input_text):
        match = re.search(r'\[Judgement\]\n(allow|deny)', input_text)
        
        if match:
            return match.group(1).strip().lower()
        else:
            return 'deny'


if __name__ == "__main__":
    layer = Layer1Aspirant(settings)
    layer.run()
    