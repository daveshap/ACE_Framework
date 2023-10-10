from ace.settings import Settings
import aio_pika

from ace.logger import Logger

logger = Logger(__name__)


async def setup_exchange(settings: Settings, channel: aio_pika.Channel, queue_name: str, durable=True):
    exchange_name = f"exchange.{queue_name}"
    logger.debug(f"Setup exchange: {exchange_name}")
    await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.FANOUT)

    queue = await channel.declare_queue(queue_name, durable=durable)
    await queue.bind(exchange_name)
    logger.debug(f"Bound {queue_name} to exchange {exchange_name}")

    if settings.system_integrity_queue and queue_name != settings.system_integrity_data_queue:
        system_integrity_queue = await channel.declare_queue(settings.system_integrity_queue, durable=True)
        await system_integrity_queue.bind(exchange_name)
        logger.debug(f"Bound {settings.system_integrity_queue} to exchange {exchange_name}")

    if settings.logging_queue:
        logging_queue = await channel.declare_queue(settings.logging_queue, durable=True)
        await logging_queue.bind(exchange_name)
        logger.debug(f"Bound {settings.logging_queue} to exchange {exchange_name}")


async def teardown_exchange(settings: Settings, channel: aio_pika.Channel, queue_name: str, durable=True):
    exchange_name = f"exchange.{queue_name}"
    logger.debug(f"Teardown exchange: {exchange_name}")

    if settings.system_integrity_queue and queue_name != settings.system_integrity_data_queue:
        system_integrity_queue = await channel.declare_queue(settings.system_integrity_queue, durable=True)
        await system_integrity_queue.unbind(exchange_name)
        await system_integrity_queue.delete()
        logger.debug(f"Removed {settings.system_integrity_queue}")

    if settings.logging_queue:
        logging_queue = await channel.declare_queue(settings.logging_queue, durable=True)
        await logging_queue.unbind(exchange_name)
        await logging_queue.delete()
        logger.debug(f"Removed {settings.logging_queue}")

    queue = await channel.declare_queue(queue_name, durable=durable)
    await queue.unbind(exchange_name)
    await queue.delete()
    logger.debug(f"Removed {queue_name}")

    exchange = await channel.get_exchange(exchange_name)
    await exchange.delete()
