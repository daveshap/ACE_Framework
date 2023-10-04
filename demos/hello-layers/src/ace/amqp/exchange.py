from ace.settings import Settings
import aio_pika


async def setup_exchange(settings: Settings, channel: aio_pika.Channel, queue_name: str):
    exchange_name = f"exchange.{queue_name}"
    await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.FANOUT)

    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.bind(exchange_name)

    if settings.system_integrity_queue:
        system_integrity_queue = await channel.declare_queue(settings.system_integrity_queue, durable=True)
        await system_integrity_queue.bind(exchange_name)

    if settings.logging_queue:
        logging_queue = await channel.declare_queue(settings.logging_queue, durable=True)
        await logging_queue.bind(exchange_name)


async def teardown_exchange(settings: Settings, channel: aio_pika.Channel, queue_name: str):
    exchange_name = f"exchange.{queue_name}"

    if settings.system_integrity_queue:
        system_integrity_queue = await channel.declare_queue(settings.system_integrity_queue, durable=True)
        await system_integrity_queue.unbind(exchange_name)
        await system_integrity_queue.delete()

    if settings.logging_queue:
        logging_queue = await channel.declare_queue(settings.logging_queue, durable=True)
        await logging_queue.unbind(exchange_name)
        await logging_queue.delete()

    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.unbind(exchange_name)
    await queue.delete()

    exchange = await channel.get_exchange(exchange_name)
    await exchange.delete()
