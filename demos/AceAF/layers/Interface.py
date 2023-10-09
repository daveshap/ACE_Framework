from . import LAYER_REGISTRY
import requests
import os
import platform
import datetime
from agentforge.utils.storage_interface import StorageInterface


class Interface:
    BASE_URL = 'http://127.0.0.1:5000/'
    storage = StorageInterface().storage_utils

    # System Information
    os_name = None
    os_version = None
    system = None
    architecture = None
    date_time = None

    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)

    def output_message(self, layer_number, message):
        url = self.BASE_URL + 'layer_update'
        data = {
            "layer_number": layer_number,
            "message": f"{message}\n"
        }

        requests.post(url, json=data)

    def get_device_info(self):
        # Operating System Information
        self.os_name = os.name
        self.os_version = platform.version()
        self.system = platform.system()
        self.architecture = platform.architecture()

    def get_current_data_time(self):
        self.date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def refresh_info(self):
        self.get_device_info()
        self.get_current_data_time()

    def get_chat_messages(self, number_messages):

        size = self.storage.count_collection("chat_history")
        qsize = max(size - number_messages, 1)
        params = {
            "collection_name": "chat_history",
            "filter": {"id": {"$gte": qsize}}
        }
        history = self.storage.load_collection(params)
        return history

    def save_chat_message(self, **kwargs):
        size = self.storage.count_collection("chat_history")
        message = f"{kwargs['respondent']}: {kwargs['message']}"
        params = {
            "collection_name": "chat_history",
            "data": [message],
            "ids": [str(size + 1)],
            "metadata": [{"id": size + 1, "respondent": kwargs['respondent']}]
        }
        self.storage.save_memory(params)
        self.output_message(0, message)

    def handle_south_bus(self, parsed_data):
        message = parsed_data['UserOutput']
        self.save_chat_message(respondent="Agent", message=message)
