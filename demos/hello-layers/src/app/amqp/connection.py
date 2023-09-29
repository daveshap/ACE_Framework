import pika
import time

from settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_connection(max_retries=5,
                   delay_factor=2,
                   host=settings.amqp_host_name,
                   username=settings.amqp_username,
                   password=settings.amqp_password,
                   heartbeat=600,
                   blocked_connection_timeout=300,
                   ):

    connection = None
    retries = 0

    while retries < max_retries:
        try:
            connection_params = pika.ConnectionParameters(
                host=host,
                heartbeat=heartbeat,
                blocked_connection_timeout=blocked_connection_timeout,
                credentials=pika.PlainCredentials(username, password),
            )
            connection = pika.BlockingConnection(connection_params)
            logger.info(f"{settings.role_name} connection established...")
            return connection
        except (pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError) as e:
            print(f"Connection attempt {retries + 1} failed with error: {e}")
            retries += 1
            time.sleep(retries * delay_factor)  # Exponential backoff

    raise Exception(f"Failed to establish a connection after maximum retries: {max_retries}.")
