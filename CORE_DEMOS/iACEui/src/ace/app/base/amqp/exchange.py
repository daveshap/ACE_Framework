from settings import settings
import aio_pika


async def create_exchange(connection: aio_pika.Connection, queue_name: str):
    channel = await connection.channel()

    logging_queue = await channel.declare_queue(settings.logging_queue, durable=True)
    exchange_name = f"exchange.{queue_name}"
    exchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.FANOUT)

    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange)

    if settings.logging_queue:
        await logging_queue.bind(exchange)

    return exchange
