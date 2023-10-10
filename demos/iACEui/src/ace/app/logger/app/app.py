from database.connection import get_db
from database.models import RabbitMQLog
from settings import settings
from init import init_db
import logging
import pika
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    with get_db() as session:
        log_entry = RabbitMQLog.from_message(method, properties, body)
        session.add(log_entry)
        try:
            session.commit()
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info("message log status: success")
        except:
            logger.info("message log status: fail")
            session.rollback()
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def get_connection(max_retries=5, delay_factor=2, username=settings.amqp_username, password=settings.amqp_password):

    connection = None
    retries = 0
    
    while retries < max_retries:
        try:
            connection_params = pika.ConnectionParameters(
                host=settings.amqp_host_name,
                heartbeat=600,
                blocked_connection_timeout=300,
                credentials=pika.PlainCredentials(username, password),
            )
            connection = pika.BlockingConnection(connection_params)
            return connection
        except (pika.exceptions.AMQPConnectionError, pika.exceptions.AMQPChannelError) as e:
            logging.info(f"Connection attempt {retries + 1} failed with error: {e}")
            retries += 1
            time.sleep(retries * delay_factor)

    raise Exception("Failed to establish a connection after maximum retries.")


def get_channel():

    conn = get_connection()
    channel = conn.channel()
    channel.queue_declare(queue=settings.logging_queue, durable=True)

    return channel


def run():
    logger.info("running logger...")
    channel = get_channel()
    channel.basic_consume(
        queue=settings.logging_queue, on_message_callback=callback, auto_ack=False
    )
    channel.start_consuming()


if __name__ == "__main__":
    init_db()
    run()
