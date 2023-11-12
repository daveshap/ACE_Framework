from .models import LayerConfig, LayerState, RabbitMQLog, AncestralPrompt, TestRun
from sqlalchemy.orm import Session
from sqlalchemy import desc
import uuid
from typing import Optional, List, Dict, Any


def get_all_test_runs(db: Session, layer_name: str):

    return (
        db.query(TestRun)
        .filter_by(layer_name=layer_name)
        .order_by(
            desc(TestRun.created_at),
        )
        .all()
    )

def store_test_results(
    db: Session,
    input: str,
    layer_name: str,
    prompts: Dict[str, str],
    source_bus: str,
    llm_messages: List[Dict[str, str]],
    llm_model_parameters: Dict[str, Any],
    reasoning_result: str,
    data_bus_action: str,
    control_bus_action: str,
    ancestral_prompt_id: uuid.UUID,
):
    new_test_run = TestRun(
        input=input,
        layer_name=layer_name,
        prompts=prompts,
        source_bus=source_bus,
        llm_messages=llm_messages,
        llm_model_parameters=llm_model_parameters,
        reasoning_result=reasoning_result,
        data_bus_action=data_bus_action,
        control_bus_action=control_bus_action,
        ancestral_prompt_id=ancestral_prompt_id,
    )
    
    db.add(new_test_run)
    db.commit()
    db.refresh(new_test_run)
    
    return new_test_run


def add_ancestral_prompt(
    db: Session,
    ancestral_prompt_id: Optional[uuid.UUID],
    prompt: str, 
    is_active: Optional[bool] = False,
):
    new_prompt = None
    current_prompt = None
    if ancestral_prompt_id:
        current_prompt = db.query(AncestralPrompt).filter_by(ancestral_prompt_id=ancestral_prompt_id).first()

    if not current_prompt:
        new_prompt = AncestralPrompt(prompt=prompt)

    else:
        new_prompt = AncestralPrompt(
            parent_ancestral_prompt_id=current_prompt.ancestral_prompt_id,
            prompt=prompt,
        )
    
    if is_active:
        db.query(AncestralPrompt).update({AncestralPrompt.is_active: False})
    
    new_prompt.is_active = is_active
    
    db.add(new_prompt)
    db.commit()
    db.refresh(new_prompt)
    
    return new_prompt

def get_active_ancestral_prompt(
    db: Session,
):
    db_prompt = db.query(AncestralPrompt).filter_by(is_active=True).first()
    return db_prompt


def get_ancestral_prompt_by_id(
    db: Session,
    ancestral_prompt_id: uuid.UUID
):
    db_prompt = db.query(AncestralPrompt).filter_by(ancestral_prompt_id=ancestral_prompt_id).first()
    return db_prompt
   

def get_ancestral_prompts(
    db: Session,
):
    db_prompt = db.query(AncestralPrompt).all()
    return db_prompt


def set_active_ancestral_prompt(
    db: Session,
    ancestral_prompt_id: uuid.UUID
):
    db_prompt = db.query(AncestralPrompt).filter_by(ancestral_prompt_id=ancestral_prompt_id).first()

    if db_prompt:
        db.query(AncestralPrompt).update({AncestralPrompt.is_active: False})
        db_prompt.is_active = True
    
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt


def get_ancestral_prompt(db: Session, ancestral_prompt_id: uuid.UUID):
    db_prompt = db.query(AncestralPrompt).filter_by(ancestral_prompt_id=ancestral_prompt_id).first()
    return db_prompt


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


def set_active_layer_config(
    db: Session,
    config_id: uuid.UUID,
):
    db_config = db.query(LayerConfig).filter(config_id == config_id).first()

    if db_config:
        db.query(LayerConfig).filter_by(
            layer_name=db_config.layer_name
        ).update({LayerConfig.is_active: False})

        db_config.is_active = True

        db.add(db_config)
        db.commit()
        db.refresh(db_config)

        return db_config


def add_layer_config(
    db: Session,
    config_id: Optional[uuid.UUID],
    layer_name: str,
    prompts,
    llm_model_parameters,
):
    layer_state = db.query(LayerState).filter_by(layer_name=layer_name).first()
    
    if not layer_state:
        layer_state = create_layer_state(
            db=db,
            layer_name=layer_name,
            process_messages=False,
        )

    db.query(LayerConfig).filter_by(
        layer_name=layer_name
    ).update({LayerConfig.is_active: False})
    
    # Ensure the specific config is deactivated
    current_config = None
    if config_id:
        current_config = (
            db.query(LayerConfig)
            .filter_by(config_id=config_id)
            .first()
        )
    if not current_config:
        new_config = LayerConfig(
            layer_name=layer_name,
            prompts=prompts,
            llm_model_parameters=llm_model_parameters,
            is_active=True
        )
    else:    
        new_config = LayerConfig(
            parent_config_id=current_config.config_id,
            layer_name=layer_name,
            prompts=prompts,
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
