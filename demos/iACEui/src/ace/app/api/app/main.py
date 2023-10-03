import asyncio
from typing import Any

import aio_pika
from fastapi import FastAPI
from pydantic import BaseModel

from settings import settings
from base.amqp.connection import get_connection
from base.amqp.exchange import create_exchange


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
    exchange = await create_exchange(connection, settings.mission_queue)

    message_body = aio_pika.Message(body=data.mission.encode())
    
    await exchange.publish(
        message_body,
        routing_key=settings.mission_queue
    )

    return {"status": "mission sent"}


@app.post("/send-mission/")
async def send_mission(data: Mission) -> Any:
    loop = asyncio.get_event_loop()
    connection = await get_connection(
        loop,
        username=settings.amqp_username,
        password=settings.amqp_password,
        amqp_host_name=settings.amqp_host_name,
    )
    exchange = await create_exchange(connection, settings.mission_queue)

    message_body = aio_pika.Message(body=data.mission.encode())
    
    await exchange.publish(
        message_body,
        routing_key=settings.mission_queue
    )

    return {"status": "mission sent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

