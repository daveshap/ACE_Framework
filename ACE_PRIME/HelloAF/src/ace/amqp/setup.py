import copy

from ace.settings import Settings
import aio_pika

from ace.logger import Logger


class AMQPSetupManager:

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

    def make_resource_pathway_name(self, resource_name, pathway):
        return self.make_exchange_name(f"pathway.{resource_name}.{pathway}")

    async def setup_exchanges(self, channel: aio_pika.Channel):
        for name, c in self.exchanges_config.items():
            config = copy.deepcopy(c)
            exchange_type = config.pop('type', 'fanout')
            durable = config.pop('durable', True)
            await self.setup_exchange(channel, name, exchange_type, durable, **config)

    async def setup_exchange(self,
                             channel: aio_pika.Channel,
                             name: str,
                             exchange_type: str = 'fanout',
                             durable: bool = True,
                             **kwargs,
                             ):
        exchange_name = self.make_exchange_name(name)
        self.log.debug(f"Set up: {exchange_name}, type: {exchange_type}, durable: {durable}, kwargs: {kwargs}")
        self.exchanges[name] = await channel.declare_exchange(exchange_name, exchange_type, durable=durable, **kwargs)

    async def teardown_exchanges(self, channel: aio_pika.Channel):
        for name, exchange in self.exchanges.items():
            await self.teardown_exchange(channel, name, exchange)

    async def teardown_exchange(self, channel: aio_pika.Channel, name: str, exchange: aio_pika.Exchange):
        await exchange.delete()
        self.log.debug(f"Tore down: {exchange.name}")

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
        for exchange, bindings in self.queue_bindings_config.items():
            for queue_name, kwargs in bindings.get('queues', {}).items():
                await self.setup_queue_binding(channel, queue_name, exchange, **kwargs)

    async def setup_queue_binding(self, channel: aio_pika.Channel, queue_name: str, exchange: str, **kwargs):
        exchange_name = self.make_exchange_name(exchange)
        await self.queues[queue_name].bind(exchange_name, **kwargs)
        self.log.debug(f"Bound queue {queue_name} to {exchange_name}, kwargs: {kwargs}")

    async def teardown_queue_bindings(self, channel: aio_pika.Channel):
        for exchange, bindings in self.queue_bindings_config.items():
            for queue_name in bindings.get('queues', {}).keys():
                await self.teardown_queue_binding(channel, queue_name, exchange)

    async def teardown_queue_binding(self, channel: aio_pika.Channel, queue_name: str, exchange: str):
        exchange_name = self.make_exchange_name(exchange)
        await self.queues[queue_name].unbind(exchange_name)
        self.log.debug(f"Unbound queue {queue_name} from {exchange_name}")

    async def setup_resource_pathways(self, channel: aio_pika.Channel):
        for name, c in self.resources_config.items():
            pathways = c.get('default_pathways', [])
            for pathway, exchanges in pathways.items():
                await self.setup_resource_pathway(channel, name, pathway, exchanges)

    async def setup_resource_pathway(self, channel: aio_pika.Channel, resource_name: str, pathway: str, exchanges: list):
        source_exchange_name = self.make_resource_pathway_name(resource_name, pathway)
        pathway = await channel.declare_exchange(source_exchange_name, aio_pika.ExchangeType.FANOUT, durable=True)
        self.resource_pathways.setdefault(resource_name, {})
        self.resource_pathways[resource_name][pathway] = {
            'pathway': pathway,
            'exchanges': exchanges,
        }
        for name in exchanges:
            exchange_name = self.make_exchange_name(name)
            await self.exchanges[name].bind(source_exchange_name)
            self.log.debug(f"Bound queue {exchange_name} to {source_exchange_name}")

    async def teardown_resource_pathways(self, channel: aio_pika.Channel):
        for name, pathways in self.resource_pathways.items():
            for pathway_data in pathways.values():
                await self.teardown_resource_pathway(channel, pathway_data)

    async def teardown_resource_pathway(self, channel: aio_pika.Channel, pathway_data: dict):
        pathway = pathway_data['pathway']
        for exchange_name in pathway_data['exchanges']:
            await self.exchanges[exchange_name].unbind(pathway.name)
            self.log.debug(f"Unbound {pathway.name} from {self.exchanges[exchange_name].name}")
        await pathway.delete()
        self.log.debug(f"Removed {pathway.name}")
