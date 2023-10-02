from ace.settings import Settings
import pika


def setup_exchange(settings: Settings, connection: pika.BlockingConnection, queue_name: str):
    channel = connection.channel()

    exchange_name = f"exchange.{queue_name}"
    channel.exchange_declare(exchange_name, exchange_type='fanout')

    channel.queue_declare(queue_name, durable=True)
    channel.queue_bind(queue_name, exchange_name)

    if settings.system_integrity_queue:
        channel.queue_declare(settings.system_integrity_queue, durable=True)
        channel.queue_bind(settings.system_integrity_queue, exchange_name)

    if settings.logging_queue:
        channel.queue_declare(settings.logging_queue, durable=True)
        channel.queue_bind(settings.logging_queue, exchange_name)


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
