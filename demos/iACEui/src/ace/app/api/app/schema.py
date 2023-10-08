from typing import List, Optional

from pydantic import BaseModel, validator
import uuid
from datetime import datetime
from constants import LAYER_NAMES, OPENAI_API_ROLES


class LayerNameBase(BaseModel):
    layer_name: str

    @validator("layer_name")
    def validate_layer_name(cls, value):
        if value not in LAYER_NAMES:
            raise ValueError(f"layer_name must be one of {LAYER_NAMES}")
        return value

# class ModelNameBase(BaseModel):
#     llm_model_name: str = 'gpt-3.5-turbo'
    
#     @validator("llm_model_name")
#     def validate_llm_model_name(cls, value):
#         if value not in LLM_MODEL_NAMES:
#             raise ValueError(f"llm_model_name must be one of {LLM_MODEL_NAMES}")
#         return value

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

    @validator("role")
    def validate_role(cls, value):
        if value not in OPENAI_API_ROLES:
            raise ValueError(f"role must be one of {OPENAI_API_ROLES}")
        return value

class LayerTestRequest(LayerNameBase, BaseModel):
    input: str
    source_bus: str
    prompts: Prompts
    llm_messages: Optional[List[LlmMessage]]
    llm_model_parameters: OpenAiGPTChatParameters

class Mission(BaseModel):
    mission: str

class LayerConfigCreate(LayerNameBase, BaseModel):
    prompts: Prompts
    llm_model_parameters: OpenAiGPTChatParameters

class LayerConfigAdd(LayerNameBase, BaseModel):
    config_id: Optional[uuid.UUID] = None # if passed it uses this as the parent config id
    prompts: Prompts
    llm_model_parameters: OpenAiGPTChatParameters

class LayerConfigDelete(BaseModel):
    config_id: uuid.UUID

class LayerStateCreate(LayerNameBase, BaseModel):
    process_messages: bool

class LayerStateUpdate(LayerNameBase, BaseModel):
    process_messages: bool

class AncestralPromptAdd(BaseModel):
    ancestral_prompt_id: Optional[uuid.UUID] = None # if passed it uses this as the parent
    prompt: str
    is_active: Optional[bool] = False

class AncestralPromptUpdate(BaseModel):
    ancestral_prompt_id: Optional[uuid.UUID]


# responses:
class LayerConfigModel(LayerNameBase, BaseModel):
    config_id: uuid.UUID
    parent_config_id: Optional[uuid.UUID] = None
    prompts: Prompts
    llm_model_parameters: OpenAiGPTChatParameters
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LayerStateModel(LayerNameBase,BaseModel):
    layer_id: uuid.UUID
    process_messages: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RabbitMQLogModel(BaseModel):
    id: uuid.UUID
    message_content: Optional[str] = None
    queue: Optional[str] = None
    source_bus: Optional[str] = None
    destination_bus: Optional[str] = None
    layer_name: Optional[str] = None
    llm_messages: Optional[List[LlmMessage]] = None
    config_id: Optional[uuid.UUID] = None
    input: Optional[str] = None
    reasoning: Optional[str] = None
    content_type: Optional[str] = None
    content_encoding: Optional[str] = None
    delivery_mode: Optional[int] = None
    priority: Optional[int] = None
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    expiration: Optional[str] = None
    message_id: Optional[str] = None
    parent_message_id: Optional[str] = None
    type: Optional[str] = None
    user_id: Optional[str] = None
    app_id: Optional[str] = None
    cluster_id: Optional[str] = None

    class Config:
        from_attributes = True


class LayerTestResponseModel(LayerNameBase, BaseModel):
    reasoning_result: LlmMessage
    data_bus_action: LlmMessage
    control_bus_action: LlmMessage
    

class ConfirmationModel(BaseModel):
    status: str = "success"

class AncestralPromptModel(BaseModel):
    ancestral_prompt_id: uuid.UUID
    parent_ancestral_prompt_id: Optional[uuid.UUID]
    prompt: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LayerTestHistoryModel(BaseModel):
    test_run_id: uuid.UUID
    input: str
    layer_name: str
    prompts: Prompts
    source_bus: str
    llm_messages: List[LlmMessage]
    llm_model_parameters: OpenAiGPTChatParameters
    reasoning_result: str
    data_bus_action: str
    control_bus_action: str
    created_at: datetime

    class Config:
        from_attributes = True
