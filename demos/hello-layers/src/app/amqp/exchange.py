from settings import settings
import pika


def create_exchange(connection: pika.BlockingConnection, queue_name: str):
    channel = connection.channel()

    logging_queue = channel.declare_queue(settings.logging_queue, durable=True)
    exchange_name = f"exchange.{queue_name}"
    exchange = channel.declare_exchange(exchange_name, exchange_type='fanout')

    queue = channel.declare_queue(queue_name, durable=True)
    queue.bind(exchange)

    if settings.logging_queue:
        logging_queue.bind(exchange)

    return exchange
