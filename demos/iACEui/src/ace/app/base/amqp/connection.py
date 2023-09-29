import aio_pika
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_connection(
    loop,
    username: str,
    password: str,
    amqp_host_name: str,
    role_name: str = "undefined",
    delay_factor=5,
    heartbeat=500,
):
    connection = None
    while True:
        try:
            connection = await aio_pika.connect_robust(
                host=amqp_host_name,
                login=username,
                password=password,
                loop=loop,
                heartbeat=heartbeat,
            )
            logger.info(f"{role_name} connection established...")
            return connection

        except Exception as e:
            logger.error(f"Error connecting to RabbitMQ: {e}. Retrying in {delay_factor} seconds...")
            await asyncio.sleep(delay_factor)
