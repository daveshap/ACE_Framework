from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, UUID, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime
import uuid
import json

from .connection import engine


Base = declarative_base()


class RabbitMQLog(Base):
    __tablename__ = "rabbitmq_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    message_content = Column(Text)
    queue = Column(String(255))

    # Headers manually added to the RabbitMQ message log
    source_bus = Column(String(50))
    parent_message_id = Column(UUID(as_uuid=True))
    destination_bus = Column(String(50))
    layer_name = Column(String(50))
    llm_messages = Column(JSON)
    config_id = Column(UUID(as_uuid=True), ForeignKey('layer_config.config_id'))
    input = Column(Text)
    reasoning = Column(Text)

    # Properties from the message's properties 
    content_type = Column(String(50))
    content_encoding = Column(String(50))
    delivery_mode = Column(Integer)
    priority = Column(Integer)
    correlation_id = Column(String(255))
    reply_to = Column(String(255))
    expiration = Column(String(50))
    message_id = Column(String(255))
    type = Column(String(50))
    user_id = Column(String(50))
    app_id = Column(String(50))
    cluster_id = Column(String(255))

    @classmethod
    def from_message(cls, method, properties, body):
        headers = properties.headers or {}

        # Deserialize Memory
        deserialized_llm_messages = None
        try:
            if headers.get('llm_messages'):
                llm_messages = headers.get('llm_messages')
                deserialized_llm_messages = json.loads(llm_messages)
        except:
            print("Error decoding JSON for llm_messages:", llm_messages)
        
        log_entry = cls(
            queue=method.routing_key,
            message_content=body.decode(),
            # Message Properties
            content_type=properties.content_type,
            content_encoding=properties.content_encoding,
            delivery_mode=properties.delivery_mode,
            priority=properties.priority,
            correlation_id=properties.correlation_id,
            reply_to=properties.reply_to,
            expiration=properties.expiration,
            message_id=properties.message_id,
            type=properties.type,
            user_id=properties.user_id,
            app_id=properties.app_id,
            cluster_id=properties.cluster_id,
            
            # Extracting and assigning header fields
            source_bus=headers.get('source_bus'),
            parent_message_id=headers.get('parent_message_id'),
            destination_bus=headers.get('destination_bus'),
            layer_name=headers.get('layer_name'),
            llm_messages=deserialized_llm_messages,
            config_id=uuid.UUID(headers.get('config_id')) if headers.get('config_id') else None,
            input=headers.get('input'),
            reasoning=headers.get('reasoning'),
        )
        
        return log_entry
    
    layer_config = relationship("LayerConfig", back_populates="rabbitmq_logs")


class LayerState(Base):
    __tablename__ = 'layer_state'

    layer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    layer_name = Column(String, nullable=False)
    process_messages = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LayerConfig(Base):
    __tablename__ = 'layer_config'

    config_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    parent_config_id = Column(UUID(as_uuid=True), nullable=True)
    layer_name = Column(String, nullable=False)
    prompts = Column(JSON, nullable=False)
    llm_model_parameters = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    rabbitmq_logs = relationship("RabbitMQLog", back_populates="layer_config")


class AncestralPrompt(Base):
    __tablename__ = 'ancestral_prompt'

    ancestral_prompt_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    parent_ancestral_prompt_id = Column(UUID(as_uuid=True), nullable=True)
    prompt = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TestRun(Base):
    __tablename__ = 'test_run'
    
    test_run_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    input = Column(String, nullable=False)
    layer_name = Column(String, nullable=False)
    prompts = Column(JSON, nullable=False)
    source_bus = Column(String, nullable=False)
    llm_messages = Column(JSON, nullable=False)
    llm_model_parameters = Column(JSON, nullable=False)
    reasoning_result = Column(Text, nullable=False)
    data_bus_action = Column(Text, nullable=False)
    control_bus_action = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    ancestral_prompt_id = Column(UUID(as_uuid=True), ForeignKey('ancestral_prompt.ancestral_prompt_id'), nullable=True)
    
    ancestral_prompt = relationship("AncestralPrompt", back_populates="test_runs")


AncestralPrompt.test_runs = relationship("TestRun", order_by=TestRun.test_run_id, back_populates="ancestral_prompt")

Base.metadata.create_all(engine)
