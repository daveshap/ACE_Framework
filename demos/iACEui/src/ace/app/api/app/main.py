import asyncio
from typing import Dict, List

import aio_pika
from fastapi import FastAPI
from settings import settings
from base.amqp.connection import get_connection
from base.amqp.exchange import create_exchange

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
import uuid
from database.connection import get_db
from database import dao

from schema import (
    LayerConfigCreate,
    LayerConfigUpdate,
    LayerStateUpdate,
    LayerStateCreate,
    Mission,
    LayerConfigModel,
    LayerStateModel,
    LayerTestRequest,
    LayerTestResponseModel,
)

from ai import generate_bus_message

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/mission")
async def send_mission(data: Mission) -> Dict[str, str]:
    loop = asyncio.get_event_loop()
    connection = await get_connection(
        loop,
        username=settings.amqp_username,
        password=settings.amqp_password,
        amqp_host_name=settings.amqp_host_name,
    )

    headers = {
        'source_bus': 'User Input',
        'destination_bus': 'Control Bus',
        'publisher': settings.role_name,
    }

    exchange = await create_exchange(connection, settings.mission_queue)

    message_body = aio_pika.Message(
        body=data.mission.encode(),
        headers=headers,
        content_type='text/plain',
    )

    await exchange.publish(
        message_body,
        routing_key=settings.mission_queue,
    )

    return {"status": "mission sent"}


@app.post("/layer/test", response_model=LayerTestResponseModel)
async def test_prompt(req: LayerTestRequest):

    reasoning_result, bus_action_result = generate_bus_message(
        input=req.prompts["input"],
        identity=req.prompts["identity"],
        reasoning=req.prompts["reasoning"],
        bus_prompt=req.prompts["bus"],
        source_bus=req.source_bus,
        desitination_bus=req.destination_bus,
        llm_messages=req.llm_messages,
        llm_model_name=req.llm_model_name,
        llm_model_parameters=req.llm_model_parameters,
        openai_api_key=settings.openai_api_key,
    )

    logger.info(f"{response}")

    results = LayerTestResponseModel(
        reasoning_result=reasoning_result,
        action_reult=bus_action_result,
    )

    return results

@app.post("/layer/config", response_model=LayerConfigModel)
def create_layer_config(
    layer_config: LayerConfigCreate,
    session: Session = Depends(get_db),
):
    try:
        with session as db:
            results = dao.create_layer_config(db, **layer_config.model_dump())
            return LayerConfigModel.model_validate(results)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=ve.args[0])

@app.get("/layer/config/{layer_name}/all", response_model=List[LayerConfigModel])
def get_all_layer_config(
    layer_name: str,
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.get_all_layer_config(db, layer_name)
        return [LayerConfigModel.model_validate(result) for result in results]


@app.get("/layer/config/{layer_name}", response_model=LayerConfigModel)
def get_layer_config(
    layer_name: str,
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.get_layer_config(db, layer_name)
        return LayerConfigModel.model_validate(results)


@app.get("/layer/logs/{layer_name}", response_model=LayerConfigModel)
def get_layer_logs(
    layer_name: str,
    session: Session = Depends(get_db),
):
    try:
        with session as db:
            results = dao.get_layer_logs(db, layer_name)
            return LayerConfigModel.model_validate(results)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ve.args[0])


@app.put("/layer/config", response_model=LayerConfigModel)
def update_layer_config(
    layer_config: LayerConfigUpdate, 
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.update_layer_config(db, **layer_config.model_dump())
        return LayerConfigModel.model_validate(results)


@app.post("/layer/state", response_model=LayerStateModel)
def create_layer_state(
    layer_state: LayerStateCreate, 
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.create_layer_state(db, **layer_state.model_dump())
        return LayerStateModel.model_validate(results)


@app.get("/layer/state/{layer_name}", response_model=LayerStateModel)
def get_layer_state_by_name(
    layer_name: str, 
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.get_layer_state_by_name(db, layer_name)
        return LayerStateModel.model_validate(results)


@app.put("/layer/state", response_model=LayerStateModel)
def update_layer_state(
    layer_state: LayerStateUpdate,
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.update_layer_state(db, **layer_state.model_dump())
        return LayerStateModel.model_validate(results)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
