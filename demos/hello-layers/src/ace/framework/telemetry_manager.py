import importlib

from ace import constants
from ace.amqp.connection import get_connection

from ace.logger import Logger

class TelemetryManager:
    def __init__(self, telemetry_classes):
        self.log = Logger(self.__class__.__name__)
        self.telemetry_classes = telemetry_classes
        self.telemetry_instances = {}
        self.load_telemetry_classes()

    def load_telemetry_classes(self):
        for class_name in self.telemetry_classes:
            try:
                module_name, class_name = class_name.rsplit('.', 1)
                module = importlib.import_module(module_name)
                class_ = getattr(module, class_name)
                self.telemetry_instances[class_name] = class_()
                self.log.debug(f"Loaded telemetry class: {class_name}")
            except Exception as e:
                self.log.error(f"Failed to load telemetry class: {class_name}. Error: {str(e)}")

    def get_telemetry(self, class_name):
        return self.telemetry_instances.get(class_name, None)

    def ingest_data(self, class_name, data):
        telemetry = self.get_telemetry(class_name)
        if telemetry:
            telemetry.ingest_data(data)
        else:
            self.log.error(f"Telemetry class not found: {class_name}")

    def retrieve_data(self, class_name, criteria):
        telemetry = self.get_telemetry(class_name)
        if telemetry:
            return telemetry.retrieve_data(criteria)
        else:
            self.log.error(f"Telemetry class not found: {class_name}")
            return None
