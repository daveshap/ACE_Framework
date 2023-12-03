import asyncio
import aio_pika

from ace.settings import Settings
from ace.logger import Logger

DEFAULT_HEARTBEAT = 600
DEFAULT_BLOCKED_CONNECTION_TIMEOUT = 300


class AMQPConnectionManager:

    def __init__(self,
                 settings: Settings,
                 ):
        self.log = Logger(self.__class__.__name__)
        self.settings = settings

    async def get_connection(self,
                             max_retries=5,
                             delay_factor=2,
                             heartbeat=DEFAULT_HEARTBEAT,
                             blocked_connection_timeout=DEFAULT_BLOCKED_CONNECTION_TIMEOUT,
                             **kwargs,
                             ):
        connection = None
        retries = 0
        while retries < max_retries:
            try:
                connection = await aio_pika.connect_robust(
                    host=self.settings.amqp_host_name,
                    login=self.settings.amqp_username,
                    password=self.settings.amqp_password,
                    heartbeat=heartbeat,
                    blocked_connection_timeout=blocked_connection_timeout,
                    **kwargs,
                )
                self.log.info(f"{self.settings.name} connection established...")
                return connection
            except (aio_pika.exceptions.AMQPConnectionError, aio_pika.exceptions.AMQPChannelError) as e:
                self.log.error(f"Connection attempt {retries + 1} failed with error: {e}")
                retries += 1
                await asyncio.sleep(retries * delay_factor)  # Exponential backoff

        raise Exception(f"Failed to establish a connection after maximum retries: {max_retries}.")
