import yaml


class ConfigParser:

    def __init__(self, config_path):
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as config_file:
            return yaml.safe_load(config_file)

    def get_resources(self):
        return self.config_data.get('resources', {})

    def get_exchanges(self):
        return self.config_data.get('exchanges', {})

    def get_queues(self):
        return self.config_data.get('queues', {})

    def get_bindings(self):
        return self.config_data.get('bindings', [])
