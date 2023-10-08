import asyncio
from typing import Dict, List
import uuid

import aio_pika
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from settings import settings
from base.amqp.connection import get_connection
from base.amqp.exchange import create_exchange

from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database.connection import get_db
from database import dao

from schema import (
    LayerConfigAdd,
    LayerStateUpdate,
    LayerStateCreate,
    Mission,
    LayerConfigModel,
    LayerStateModel,
    LayerTestRequest,
    LayerTestResponseModel,
    LlmMessage,
    AncestralPromptAdd,
    AncestralPromptModel,
)

from ai import generate_bus_message

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = ["http://localhost:5173", "http://0.0.0.0:5173", "http://192.168.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,  # Allow cookies, headers, etc.
    allow_methods=["*"],     # Allow all methods
    allow_headers=["*"],     # Allow all headers
)

@app.options("/{path:path}")
async def handle_options_request(path: str, response: Response):
    response.status_code = status.HTTP_200_OK
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


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
        "source_bus": "User Input",
        "destination_bus": "Control Bus",
        "publisher": settings.role_name,
    }

    exchange = await create_exchange(connection, settings.mission_queue)

    message_body = aio_pika.Message(
        body=data.mission.encode(),
        headers=headers,
        content_type="text/plain",
    )

    await exchange.publish(
        message_body,
        routing_key=settings.mission_queue,
    )

    return {"status": "mission sent"}


@app.post("/layer/test", response_model=LayerTestResponseModel)
async def test_prompt(req: LayerTestRequest, session: Session = Depends(get_db)):
    reasoning_response, data_bus_action, control_bus_action = generate_bus_message(
        input=req.input,
        layer_name=req.layer_name,
        prompts=req.prompts,
        source_bus=req.source_bus,
        llm_messages=req.llm_messages if req.llm_messages else [],
        llm_model_parameters=req.llm_model_parameters,
        openai_api_key=settings.openai_api_key,
    )
    with session as db:
        dao.store_test_results(
            **req.model_dump(),
            reasoning_result=reasoning_response['content'],
            data_bus_action=data_bus_action['content'],
            control_bus_action=control_bus_action['content'],
            db=db,
        )

    reasoning_result = LlmMessage(**reasoning_response)
    data_bus_action = LlmMessage(**data_bus_action)
    control_bus_action = LlmMessage(**control_bus_action)

    results = LayerTestResponseModel(
        layer_name=req.layer_name,
        reasoning_result=reasoning_result,
        data_bus_action=data_bus_action,
        control_bus_action=control_bus_action,
    )

    return results


@app.post("/prompt/ancestral", response_model=AncestralPromptModel)
def add_ancestral_prompt(
    ancestral_prompt: AncestralPromptAdd,
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.add_ancestral_prompt(db=db, **ancestral_prompt.model_dump())
        return AncestralPromptModel.model_validate(results)


@app.patch(
    "/prompt/ancestral/{ancestral_prompt_id}/active",
    response_model=AncestralPromptModel,
)
def set_active_ancestral_prompt(
    ancestral_prompt_id: uuid.UUID,
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.set_active_ancestral_prompt(
            db=db,
            ancestral_prompt_id=ancestral_prompt_id,
        )
        return AncestralPromptModel.model_validate(results)


@app.get("/prompt/ancestral/{ancestral_prompt_id}", response_model=AncestralPromptAdd)
def get_active_ancestral_prompt(
    ancestral_prompt_id: uuid.UUID,
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.get_ancestral_prompt(
            db=db, ancestral_prompt_id=ancestral_prompt_id
        )
        return AncestralPromptModel.model_validate(results)


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


@app.post("/layer/config", response_model=LayerConfigModel)
def add_layer_config(
    layer_config: LayerConfigAdd,
    session: Session = Depends(get_db),
):
    try:
        with session as db:
            results = dao.add_layer_config(db, **layer_config.model_dump())
            return LayerConfigModel.model_validate(results)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])


@app.patch("/layer/config/{config_id}/active", response_model=LayerConfigModel)
def set_active_config(
    config_id: uuid.UUID,
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.set_active_layer_config(db=db, config_id=config_id)
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


@app.patch("/layer/state/{layer_name}/pause", response_model=LayerStateModel)
def update_layer_state(
    layer_name: str,
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.update_layer_state(
            db=db,
            layer_name=layer_name,
            process_messages=False,
        )
        return LayerStateModel.model_validate(results)


@app.patch("/layer/state/{layer_name}/resume", response_model=LayerStateModel)
def update_layer_state(
    layer_name: str,
    session: Session = Depends(get_db),
):
    with session as db:
        results = dao.update_layer_state(
            db=db,
            layer_name=layer_name,
            process_messages=True,
        )
        return LayerStateModel.model_validate(results)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
