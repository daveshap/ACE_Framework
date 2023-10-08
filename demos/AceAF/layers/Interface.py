from . import LAYER_REGISTRY
import requests
import os
import platform
import datetime


class Interface:
    BASE_URL = 'http://127.0.0.1:5000/'

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
            "message": message
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
