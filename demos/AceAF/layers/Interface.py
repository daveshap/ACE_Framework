from . import LAYER_REGISTRY
import requests


class Interface:
    BASE_URL = 'http://127.0.0.1:5000/'

    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)

    def output_message(self, layer_number, message):
        url = self.BASE_URL + 'layer_update'
        data = {
            "layer_number": layer_number,
            "message": message
        }

        requests.post(url, json=data)
