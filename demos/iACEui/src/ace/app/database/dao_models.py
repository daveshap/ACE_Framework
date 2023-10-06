from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class RabbitMQLogModel(BaseModel):
    id: UUID
    message_content: str
    queue: str
    source_bus: Optional[str]
    destination_bus: Optional[str]
    layer_name: str
    llm_messages: Optional[dict]
    layer_config_id: UUID
    source_message_id: Optional[UUID]
    content_type: Optional[str]
    content_encoding: Optional[str]
    delivery_mode: Optional[int]
    priority: Optional[int]
    correlation_id: Optional[str]
    reply_to: Optional[str]
    expiration: Optional[str]
    message_id: Optional[str]
    type: Optional[str]
    user_id: Optional[str]
    app_id: Optional[str]
    cluster_id: Optional[str]

class LayerConfigModel(BaseModel):
    config_id: UUID
    layer_id: UUID
    layer_name: str
    prompts: dict
    llm_model_name: str
    llm_model_parameters: dict
    is_active: bool
    created_at: datetime
    updated_at: datetime

class MessageWithLayerConfigModel(BaseModel):
    rabbitmq_log: RabbitMQLogModel
    layer_config: LayerConfigModel
