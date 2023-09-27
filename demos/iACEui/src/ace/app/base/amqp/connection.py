import aio_pika
import asyncio

from settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_connection(
    loop,
    delay_factor=5,
    heartbeat=500,
    username=settings.amqp_username,
    password=settings.amqp_password,
):
    connection = None
    while True:
        try:
            connection = await aio_pika.connect_robust(
                host=settings.amqp_host_name,
                login=username,
                password=password,
                loop=loop,
                heartbeat=heartbeat,
            )
            logger.info(f"{settings.role_name} connection established...")
            return connection

        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}. Retrying in {delay_factor} seconds...")
            await asyncio.sleep(delay_factor)
