from pydantic import BaseModel, model_validator, ValidationError, RootModel
from typing import Dict, Any, Optional, List
import yaml
from pathlib import Path

from ace.logger import Logger

REQUIRED_CONFIG_SECTIONS = ('resources', 'exchanges', 'queues', 'bindings')
DEFAULT_CONFIG_FILE_PATH = Path(__file__).parent / 'messaging_config.yaml'

ExchangesModel = RootModel[Dict[str, Dict[str, Any]]]
QueuesModel = RootModel[Dict[str, Dict[str, Any]]]


class ResourcesModel(BaseModel):
    subscribes_to: Optional[Dict[str, str]] = {}
    restricted_publish_exchanges: Optional[List[str]] = []
    default_pathways: Optional[Dict[str, List[str]]] = {}


class BindingsModel(BaseModel):
    queues: Optional[Dict[str, Dict[str, Any]]] = {}
    exchanges: Optional[Dict[str, Dict[str, Any]]] = {}


class ConfigModel(BaseModel):
    resources: Dict[str, ResourcesModel]
    exchanges: ExchangesModel
    queues: QueuesModel
    bindings: Dict[str, BindingsModel]

    @model_validator(mode='before')
    @classmethod
    def check_required_sections(cls, data):
        for section in REQUIRED_CONFIG_SECTIONS:
            if section not in data or data[section] is None:
                raise ValueError(f"Missing required configuration section: {section}")
        return data


class ConfigParser:
    def __init__(self, config_path: str = DEFAULT_CONFIG_FILE_PATH):
        self.log = Logger(self.__class__.__name__)
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self) -> ConfigModel:
        if not Path(self.config_path).is_file():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        with open(self.config_path, 'r') as config_file:
            try:
                config_data = yaml.safe_load(config_file)
            except yaml.YAMLError as e:
                raise ValueError(f"Error parsing YAML configuration: {e}")
        try:
            return ConfigModel(**config_data)
        except ValidationError as e:
            raise ValueError(f"Validation error for configuration data: {e}")

    def get_resources(self) -> Dict[str, ResourcesModel]:
        return self.config_data.resources

    def get_exchanges(self) -> Dict[str, Dict[str, Any]]:
        return self.config_data.exchanges.root

    def get_queues(self) -> Dict[str, Dict[str, Any]]:
        return self.config_data.queues.root

    def get_bindings(self) -> Dict[str, BindingsModel]:
        return self.config_data.bindings
