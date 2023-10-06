from .models import LayerConfig, LayerState, RabbitMQLog
from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid
from typing import Optional


def create_layer_config(db: Session, layer_name: str, prompts: dict, llm_model_name: str, llm_model_parameters: dict):
    layer = db.query(LayerState).filter_by(layer_name=layer_name).first()
    
    if not layer:
        layer = create_layer_state(
            db=db,
            layer_name=layer_name,
            process_messages=False,
        )

    config = db.query(LayerConfig).first()

    if config:
        raise ValueError(f"Layer config for '{layer_name}' already exists, use update api")

    new_config = LayerConfig(
        layer_name=layer_name,
        prompts=prompts,
        llm_model_name=llm_model_name,
        llm_model_parameters=llm_model_parameters,
        is_active=True
    )
    
    db.add(new_config)
    db.commit()
    return new_config


def get_layer_logs(db: Session, layer_name: str):
    
    logs_and_config = (
        db.query(RabbitMQLog, LayerConfig)
        .join(LayerConfig, RabbitMQLog.config_id == LayerConfig.config_id)
        .filter(LayerConfig.layer_name == layer_name)
        .all()
    )

    if not logs_and_config:
        raise ValueError("No logs found for layer_name: {}".format(layer_name))

    return logs_and_config


def update_layer_config(
    db: Session,
    config_id: uuid.UUID, 
    layer_name: str, 
    prompts, 
    llm_model_name, 
    llm_model_parameters,
):
    db.query(LayerConfig).filter_by(
        layer_name=layer_name
    ).update({LayerConfig.is_active: False})
    
    # Ensure the specific config is deactivated
    current_config = (
        db.query(LayerConfig)
        .filter_by(config_id=config_id)
        .first()
    )
    if not current_config:
        raise ValueError("LayerConfig not found")
    
    new_config = LayerConfig(
        parent_config_id=current_config.config_id,
        layer_name=layer_name,
        prompts=prompts,
        llm_model_name=llm_model_name,
        llm_model_parameters=llm_model_parameters,
        is_active=True
    )
    
    db.add(new_config)
    db.commit()
    db.refresh(new_config)

    return new_config


def get_all_layer_config(db: Session, layer_name: str):
    return (
        db.query(LayerConfig)
        .filter_by(layer_name=layer_name)
        .order_by(
            desc(LayerConfig.is_active),
            desc(LayerConfig.updated_at)
        )
        .all()
    )

def get_layer_config(db: Session, layer_name: str):
    return (
        db.query(LayerConfig)
        .filter_by(layer_name=layer_name)
        .filter_by(is_active=True)
        .first()
    )


def create_layer_state(db: Session, layer_name: str, process_messages: bool = False):
    db_layer_state = LayerState(layer_name=layer_name, process_messages=process_messages)
    db.add(db_layer_state)
    db.commit()
    db.refresh(db_layer_state)
    return db_layer_state


def get_layer_state_by_name(db: Session, layer_name: str):

    layer_state = db.query(LayerState).filter(LayerState.layer_name == layer_name).first()
    
    if not layer_state:
        layer_state = LayerState(layer_name=layer_name)
        db.add(layer_state)
        db.commit()
    
    return layer_state


def update_layer_state(
        db: Session,
        process_messages: bool,
        layer_name: Optional[str] = None
):
    if layer_name is not None:
        db_layer_state = db.query(LayerState).filter(LayerState.layer_name == layer_name).first()
    else:
        raise ValueError("Layer_name must be provided.")
    
    if not db_layer_state:
        db_layer_state = LayerState(layer_name=layer_name)
        db.add(db_layer_state)
        db.commit()
    
    db_layer_state.process_messages = process_messages
    db.commit()
    db.refresh(db_layer_state)
    return db_layer_state
