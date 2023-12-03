import copy

from ace.settings import Settings
import aio_pika

from ace.logger import Logger

EXCHANGE_TYPE_MAP = {
    'fanout': aio_pika.ExchangeType.FANOUT,
    'topic': aio_pika.ExchangeType.TOPIC,
    'direct': aio_pika.ExchangeType.DIRECT
}


class Setup:

    def __init__(self, settings: Settings, resources_config, exchanges_config, queues_config, queue_bindings_config):
        self.log = Logger(self.__class__.__name__)
        self.settings = settings
        self.resources_config = resources_config
        self.exchanges_config = exchanges_config
        self.queues_config = queues_config
        self.queue_bindings_config = queue_bindings_config
        self.exchanges = {}
        self.queues = {}
        self.queue_bindings = []
        self.resource_pathways = {}

    def make_exchange_name(self, name):
        return f"exchange.{name}"

    def make_resource_pathway_name(self, name):
        return self.make_exchange_name(f"pathway.{name}")

    async def setup_exchanges(self, channel: aio_pika.Channel):
        for name, c in self.exchanges_config.items():
            config = copy.deepcopy(c)
            exchange_type = config.pop('type', 'fanout')
            await self.setup_exchange(channel, name, exchange_type, **config)

    async def setup_exchange(self, channel: aio_pika.Channel, name: str, exchange_type: str = 'fanout', **kwargs):
        exchange_name = self.make_exchange_name(name)
        self.log.debug(f"Set up exchange: {exchange_name}, type: {exchange_type}, kwargs: {kwargs}")
        self.exchanges[name] = await channel.declare_exchange(exchange_name, EXCHANGE_TYPE_MAP[exchange_type], **kwargs)
        if exchange_type == 'fanout':
            self.bind_monitoring_queues(channel, exchange_name)

    async def teardown_exchanges(self, channel: aio_pika.Channel, exchange: aio_pika.Exchange):
        for exchange in self.exchanges.values():
            await self.teardown_exchange(channel, exchange)
        self.teardown_monitoring_queues(channel)

    async def teardown_exchange(self, channel: aio_pika.Channel, exchange: aio_pika.Exchange):
        # NOTE: exchange._type is not public, but convenient for this task
        if exchange._type == 'fanout':
            self.unbind_monitoring_queues(channel, exchange.name)
        await exchange.delete()
        self.log.debug(f"Tore down exchange: {exchange.name}")

    async def teardown_monitoring_queues(self, channel: aio_pika.Channel):
        if self.settings.system_integrity_queue:
            system_integrity_queue = await channel.declare_queue(self.settings.system_integrity_queue, durable=True)
            await system_integrity_queue.delete(if_empty=False, if_unused=False)
            self.log.debug(f"Removed queue {self.settings.system_integrity_queue}")
        if self.settings.logging_queue:
            logging_queue = await channel.declare_queue(self.settings.logging_queue, durable=True)
            await logging_queue.delete(if_empty=False, if_unused=False)
            self.log.debug(f"Removed queue {self.settings.logging_queue}")

    async def bind_monitoring_queues(self, channel: aio_pika.Channel, exchange_name):
        if self.settings.system_integrity_queue:
            system_integrity_queue = await channel.declare_queue(self.settings.system_integrity_queue, durable=True)
            await system_integrity_queue.bind(exchange_name)
            self.log.debug(f"Bound {self.settings.system_integrity_queue} to exchange {exchange_name}")

        if self.settings.logging_queue:
            logging_queue = await channel.declare_queue(self.settings.logging_queue, durable=True)
            await logging_queue.bind(exchange_name)
            self.log.debug(f"Bound {self.settings.logging_queue} to exchange {exchange_name}")

    async def unbind_monitoring_queues(self, channel: aio_pika.Channel, exchange_name: str):
        if self.settings.system_integrity_queue:
            system_integrity_queue = await channel.declare_queue(self.settings.system_integrity_queue, durable=True)
            await system_integrity_queue.unbind(exchange_name)
            self.log.debug(f"Unbound {self.settings.system_integrity_queue}")
        if self.settings.logging_queue:
            logging_queue = await channel.declare_queue(self.settings.logging_queue, durable=True)
            await logging_queue.unbind(exchange_name)
            self.log.debug(f"Unbound {self.settings.logging_queue}")

    async def setup_queues(self, channel: aio_pika.Channel):
        for name, c in self.queues_config.items():
            config = copy.deepcopy(c)
            durable = config.pop('durable', True)
            arguments = config.pop('arguments', {})
            await self.setup_queue(channel, name, durable, arguments, **config)

    async def setup_queue(self, channel: aio_pika.Channel, name: str, durable: bool = True, arguments: dict = None, **kwargs):
        arguments = arguments or {}
        self.queues[name] = await channel.declare_queue(
            name,
            durable=durable,
            arguments=arguments,
            **kwargs,
        )
        self.log.debug(f"Declared queue {name}, durable: {durable}, arguments: {arguments}, kwargs: {kwargs}")

    async def teardown_queues(self, channel: aio_pika.Channel):
        for queue in self.queues.values():
            await self.teardown_queue(channel, queue)

    async def teardown_queue(self, channel: aio_pika.Channel, queue: aio_pika.Queue):
        await queue.delete(if_empty=False, if_unused=False)
        self.log.debug(f"Removed queue {queue.name}, durable: {queue.durable}")

    async def setup_queue_bindings(self, channel: aio_pika.Channel):
        for binding in self.queue_bindings_config:
            config = copy.deepcopy(binding)
            queue_name = config.pop('queue')
            exchange_name = config.pop('exchange')
            await self.setup_queue_binding(channel, queue_name, exchange_name, **config)

    async def setup_queue_binding(self, channel: aio_pika.Channel, queue_name: str, exchange_name: str, **kwargs):
        await self.queues[queue_name].bind(self.make_exchange_name(exchange_name), **kwargs)
        self.queue_bindings.append({
            'queue': queue_name,
            'exchange': exchange_name,
        })
        self.log.debug(f"Bound queue {queue_name} to exchange {exchange_name}, kwargs: {kwargs}")

    async def teardown_queue_bindings(self, channel: aio_pika.Channel):
        for binding in self.queue_bindings:
            await self.teardown_queue_binding(channel, binding['queue'], binding['exchange'])

    async def teardown_queue_binding(self, channel: aio_pika.Channel, queue_name: str, exchange_name: str):
        await self.queues[queue_name].unbind(self.make_exchange_name(exchange_name))
        self.log.debug(f"Unbound queue {queue_name} from exchange {exchange_name}")

    async def setup_resource_pathways(self, channel: aio_pika.Channel):
        for name, c in self.resources_config.items():
            pathways = c.get('default_pathways', [])
            for pathway, exchanges in pathways.items():
                await self.setup_resource_pathway(channel, name, pathway, exchanges)

    async def setup_resource_pathway(self, channel: aio_pika.Channel, resource_name: str, pathway: str, exchanges: list):
        source_exchange_name = self.make_resource_pathway_name(pathway)
        pathway = await channel.declare_exchange(source_exchange_name, aio_pika.ExchangeType.FANOUT)
        self.resource_pathways.setdefault(resource_name, {})
        self.resource_pathways[resource_name][pathway] = {
            'pathway': pathway,
            'exchanges': exchanges,
        }
        for name in exchanges:
            exchange_name = self.make_exchange_name(name)
            await self.exchanges[name].bind(source_exchange_name)
            self.log.debug(f"Bound queue {exchange_name} to exchange {source_exchange_name}")

    async def teardown_resource_pathways(self, channel: aio_pika.Channel):
        for name, pathways in self.resource_pathways:
            for pathway_data in pathways.values():
                await self.teardown_resource_pathway(channel, pathway_data)

    async def teardown_resource_pathway(self, channel: aio_pika.Channel, pathway_data: dict):
        pathway = pathway_data['pathway']
        for exchange_name in pathway_data['exchanges']:
            await self.exchanges[exchange_name].unbind(pathway.name)
            self.log.debug(f"Unbound exchange {pathway.name} from exchange {self.exchanges[exchange_name].name}")
        await pathway.delete()
        self.log.debug(f"Removed exchange {pathway.name}")
