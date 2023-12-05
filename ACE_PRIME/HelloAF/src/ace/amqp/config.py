from pydantic import BaseModel, validator, ValidationError
from typing import Dict, Any, Optional
import yaml
from pathlib import Path


class ResourcesModel(BaseModel):
    subscribes_to: Optional[list]
    restricted_publish_exchanges: Optional[list]
    default_pathways: Optional[dict]


class ExchangesModel(BaseModel):
    __root__: Dict[str, Dict[str, Any]]


class QueuesModel(BaseModel):
    __root__: Dict[str, Dict[str, Any]]


class BindingsModel(BaseModel):
    queues: Optional[Dict[str, Dict[str, Any]]]
    exchanges: Optional[Dict[str, Dict[str, Any]]]


class ConfigModel(BaseModel):
    resources: Dict[str, ResourcesModel]
    exchanges: ExchangesModel
    queues: QueuesModel
    bindings: Dict[str, BindingsModel]

    @validator('resources', 'exchanges', 'queues', 'bindings', pre=True, each_item=True)
    def check_required_sections(cls, v, field):
        if v is None:
            raise ValueError(f"Missing required configuration section: {field.name}")
        return v


class ConfigParser:
    def __init__(self, config_path: str):
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
        return self.config_data.exchanges.__root__

    def get_queues(self) -> Dict[str, Dict[str, Any]]:
        return self.config_data.queues.__root__

    def get_bindings(self) -> Dict[str, BindingsModel]:
        return self.config_data.bindings
