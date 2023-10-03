import pika
from sqlalchemy import Column, Integer, String, DateTime, Sequence, DDL, text, Text, UUID, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid
import json


# SQLAlchemy setup
Base = declarative_base()


class RabbitMQLog(Base):
    __tablename__ = "rabbitmq_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    message_content = Column(Text)

    # Message content and topic (routing key)
    queue = Column(String(255))

    # Headers if the team will be using them.
    source_bus = Column(String(50)) # Data or Control
    destination_bus = Column(String(50)) # Data or Control
    publisher = Column(String(50)) # The layer that published the message (settings.role_name)
    layer_memory = Column(JSON) # The context or memory in the layer at the time of the message being sent
    model = Column(String(50)) # The LLM model used to generate the message

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
        deserialized_memory = None
        try:
            if headers.get('layer_memory'):
                serialized_memory = headers.get('layer_memory')
                deserialized_memory = json.loads(serialized_memory)
        except:
            # TODO add logs
            pass
        
        log_entry = cls(
            queue=method.routing_key,
            message_content=body.decode(),
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
            destination_bus=headers.get('destination_bus'),
            publisher=headers.get('publisher'),
            layer_memory=deserialized_memory,
            model=headers.get('model')
        )
        
        return log_entry
