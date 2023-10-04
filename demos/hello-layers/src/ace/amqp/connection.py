import asyncio
import aio_pika

from ace.settings import Settings
from ace.logger import Logger

logger = Logger(__name__)


async def get_connection_and_channel(settings: Settings,
                                     loop=asyncio.get_event_loop(),
                                     max_retries=5,
                                     delay_factor=2,
                                     heartbeat=600,
                                     blocked_connection_timeout=300,
                                     ):

    host = settings.amqp_host_name
    username = settings.amqp_username
    password = settings.amqp_password
    connection = None
    retries = 0

    while retries < max_retries:
        try:
            connection = await aio_pika.connect_robust(
                f"amqp://{username}:{password}@{host}",
                heartbeat=heartbeat,
                blocked_connection_timeout=blocked_connection_timeout,
            )
            channel = await connection.channel()  # Create a new channel
            logger.info(f"{settings.name} connection and channel established...")
            return connection, channel
        except (aio_pika.exceptions.AMQPConnectionError, aio_pika.exceptions.AMQPChannelError) as e:
            print(f"Connection attempt {retries + 1} failed with error: {e}")
            retries += 1
            await asyncio.sleep(retries * delay_factor)  # Exponential backoff

    raise Exception(f"Failed to establish a connection and channel after maximum retries: {max_retries}.")
