from . import LAYER_REGISTRY
import requests


class Interface:
    BASE_URL = 'http://127.0.0.1:5000/'

    def output_message(self, layer_number, message):
        url = self.BASE_URL + 'layer_update'
        data = {
            "layer_number": layer_number,
            "message": message
        }

        response = requests.post(url, json=data)

        # url = self.BASE_URL + target
        # print(f"\nSending message to {url}: {message}")
        # response = requests.post(url, json={'message': message})
        # print(f"\nResponse: {response}")

        return response.json()

    def handle_incoming(self):
        pass

    def collect_user_chat(self, message):
        # Process the user message
        # ...
        # Tag and store the message
        self.store_message(message, tag="new_input")
        # Trigger event for the relevant layer (e.g., L1)
        # LAYER_REGISTRY[1].event.set()

    def store_message(self, message, tag):
        # Store the message with the given tag
        pass
