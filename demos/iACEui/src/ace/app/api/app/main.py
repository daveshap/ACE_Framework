import asyncio
from typing import Any, Dict, List

import aio_pika
from fastapi import FastAPI
from pydantic import BaseModel

from settings import settings
from base.amqp.connection import get_connection
from base.amqp.exchange import create_exchange

from ai import generate_completion
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class Mission(BaseModel):
    mission: str


@app.post("/send-mission/")
async def send_mission(data: Mission) -> Any:
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

class IdentityTestRequest(BaseModel):
    identity: str
    message: str
    memory: List[Dict[Any,Any]] = []
    model: str = 'gpt-3.5-turbo'
    temperature: int = 0

class IdentityTestResponse(BaseModel):
    identity: str
    message: str
    memory: List[Dict[Any,Any]] = []
    model: str = 'gpt-3.5-turbo'
    response: Dict[str, str]


@app.post("/test/identity", response_model=IdentityTestResponse)
async def test_prompt(req: IdentityTestRequest) -> Any:

    response, memory = generate_completion(
        identity=req.identity,
        new_message=req.message,
        memory=req.memory,
        model=req.model,
        temperature=req.temperature,
        openai_api_key=settings.openai_api_key
    )

    logger.info(f"{response}")

    resp = IdentityTestResponse(
        identity=req.identity,
        message=req.message,
        memory=memory,
        model=req.model,
        response=response,
    )

    return resp



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

