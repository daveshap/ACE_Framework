from pydantic import BaseModel, validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime
import json

LAYER_NAMES = [
    "Aspirational Layer",
    "Global Strategy Layer",
    "Agent Model Layer",
    "Executive Layer",
    "Cognitive Control Layer",
    "Task Prosecution Layer",
]

class LayerNameBase(BaseModel):
    layer_name: str

    @validator("layer_name")
    def validate_layer_name(cls, value):
        if value not in LAYER_NAMES:
            raise ValueError(f"layer_name must be one of {LAYER_NAMES}")
        return value

class OpenAiGPTChatParameters(BaseModel):
    model: str = 'gpt-3.5-turbo'
    temperature: float = 0.0
    max_tokens: int = 512
    top_p: Optional[float]
    frequency_penalty: Optional[float]
    presence_penalty: Optional[float]

class Prompts(BaseModel):
    identity: str
    reasoning: str
    data_bus: str
    control_bus: str

class LlmMessage(BaseModel):
    role: str
    content: str

class RabbitMQLogModel(LayerNameBase, BaseModel):
    id: UUID
    message_content: str
    queue: str

    # Headers
    source_bus: Optional[str]
    parent_message_id: Optional[UUID]
    destination_bus: Optional[str]
    layer_name: Optional[str]
    llm_messages: Optional[List[LlmMessage]]
    config_id: UUID
    input: Optional[str]
    reasoning: Optional[str]

    # Properties from the message's properties 
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

    @classmethod
    def from_string(cls, record: str):
        # Assuming the record string is a serialized JSON
        data = json.loads(record)
        return cls(**data)

class LayerConfigModel(LayerNameBase, BaseModel):
    config_id: UUID
    parent_config_id: Optional[UUID] = None
    layer_name: str
    prompts: Prompts
    llm_model_parameters: OpenAiGPTChatParameters
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageWithLayerConfigModel(BaseModel):
    rabbitmq_log: RabbitMQLogModel
    layer_config: LayerConfigModel

class AncestralPromptModel(BaseModel):
    ancestral_prompt_id: UUID
    parent_ancestral_prompt_id: Optional[UUID]
    prompt: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
