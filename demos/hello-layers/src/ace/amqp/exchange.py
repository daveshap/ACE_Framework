from ace.settings import Settings
import pika


def setup_exchange(settings: Settings, connection: pika.BlockingConnection, queue_name: str):
    channel = connection.channel()

    exchange_name = f"exchange.{queue_name}"
    exchange = channel.declare_exchange(exchange_name, exchange_type='fanout')

    queue = channel.declare_queue(queue_name, durable=True)
    queue.bind(exchange)

    if settings.system_integrity_queue:
        system_integrity_queue = channel.declare_queue(settings.system_integrity_queue, durable=True)
        system_integrity_queue.bind(exchange)

    if settings.logging_queue:
        logging_queue = channel.declare_queue(settings.logging_queue, durable=True)
        logging_queue.bind(exchange)

    return exchange


def teardown_exchange(settings: Settings, connection: pika.BlockingConnection, queue_name: str):
    channel = connection.channel()

    exchange_name = f"exchange.{queue_name}"

    if settings.system_integrity_queue:
        channel.queue_unbind(queue=settings.system_integrity_queue, exchange=exchange_name)
        channel.queue_delete(queue=settings.system_integrity_queue)

    if settings.logging_queue:
        channel.queue_unbind(queue=settings.logging_queue, exchange=exchange_name)
        channel.queue_delete(queue=settings.logging_queue)

    channel.queue_unbind(queue=queue_name, exchange=exchange_name)
    channel.queue_delete(queue=queue_name)

    channel.exchange_delete(exchange=exchange_name)
