import yaml
from pathlib import Path
from typing import Dict, List, Any

REQUIRED_SECTIONS = ['resources', 'exchanges', 'queues', 'bindings']


class ConfigParser:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if not Path(self.config_path).is_file():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        with open(self.config_path, 'r') as config_file:
            try:
                config_data = yaml.safe_load(config_file)
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing YAML configuration: {e}")
        self.validate_config(config_data)
        return config_data

    def validate_config(self, config_data: Dict[str, Any]):
        for section in REQUIRED_SECTIONS:
            if section not in config_data:
                raise ValueError(f"Missing required configuration section: {section}")
        # TODO: Add more specific validation rules as needed

    def get_resources(self) -> Dict[str, Dict[str, List[str]]]:
        return self.config_data['resources']

    def get_exchanges(self) -> Dict[str, List[str]]:
        return self.config_data['exchanges']

    def get_queues(self) -> Dict[str, List[str]]:
        return self.config_data['queues']

    def get_bindings(self) -> List[Dict[str, str]]:
        return self.config_data['bindings']
