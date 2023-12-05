from pydantic import BaseModel
from typing import Dict, List, Union, Any
from pydantic.fields import Field

from ace.settings import Settings
from ace.amqp.config import ConfigModel
import aio_pika

from ace.logger import Logger


class ExchangeConfig(BaseModel):
    type: aio_pika.ExchangeType = 'fanout'
    durable: bool = True

    class Config:
        extra = 'allow'  # Allow extra fields for additional exchange configuration


class QueueConfig(BaseModel):
    durable: bool = True
    arguments: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = 'allow'


class AMQPSetupManager:

    def __init__(self, settings: Settings, config: ConfigModel):
        self.log = Logger(self.__class__.__name__)
        self.settings = settings
        self.config = config
        self.exchanges: Dict[str, aio_pika.Exchange] = {}
        self.queues: Dict[str, aio_pika.Queue] = {}
        self.resource_pathways: Dict[str, Dict[str, Dict[str, Union[aio_pika.Exchange, List[str]]]]] = {}

    def make_exchange_name(self, name: str):
        return f"exchange.{name}"

    def make_resource_pathway_name(self, resource_name: str, pathway: str):
        return self.make_exchange_name(f"pathway.{resource_name}.{pathway}")

    async def setup_exchanges(self, channel: aio_pika.Channel):
        for name, config in self.config.get_exchanges().items():
            self.setup_exchange(channel, name, ExchangeConfig(**config))

    async def setup_exchange(self,
                             channel: aio_pika.Channel,
                             name: str,
                             config: ExchangeConfig
                             ):
        exchange_name = self.make_exchange_name(name)
        self.log.debug(f"Set up: {exchange_name}, config: {config}")
        self.exchanges[name] = await channel.declare_exchange(
            exchange_name,
            **config.model_dump(exclude_unset=True, exclude_none=True),
        )

    async def teardown_exchanges(self, channel: aio_pika.Channel):
        for name, exchange in self.exchanges.items():
            await self.teardown_exchange(channel, name, exchange)

    async def teardown_exchange(self, channel: aio_pika.Channel, name: str, exchange: aio_pika.Exchange):
        await exchange.delete()
        self.log.debug(f"Tore down: {exchange.name}")

    async def setup_queues(self, channel: aio_pika.Channel):
        for name, config in self.config.get_queues().items():
            await self.setup_queue(channel, name, QueueConfig(**config))

    async def setup_queue(self, channel: aio_pika.Channel, name: str, config: QueueConfig):
        self.queues[name] = await channel.declare_queue(
            name,
            **config.model_dump(exclude_unset=True, exclude_none=True),
        )
        self.log.debug(f"Declared queue {name}, config: {config}")

    async def teardown_queues(self, channel: aio_pika.Channel):
        for queue in self.queues.values():
            await self.teardown_queue(channel, queue)

    async def teardown_queue(self, channel: aio_pika.Channel, queue: aio_pika.Queue):
        await queue.delete(if_empty=False, if_unused=False)
        self.log.debug(f"Removed queue {queue.name}, durable: {queue.durable}")

    async def setup_queue_bindings(self, channel: aio_pika.Channel):
        for exchange, bindings in self.config.get_bindings().items():
            queues = bindings.queues or {}
            for queue_name, kwargs in queues.items():
                await self.setup_queue_binding(channel, queue_name, exchange, **kwargs)

    async def setup_queue_binding(self, channel: aio_pika.Channel, queue_name: str, exchange: str, **kwargs):
        exchange_name = self.make_exchange_name(exchange)
        await self.queues[queue_name].bind(exchange_name, **kwargs)
        self.log.debug(f"Bound queue {queue_name} to {exchange_name}, kwargs: {kwargs}")

    async def teardown_queue_bindings(self, channel: aio_pika.Channel):
        for exchange, bindings in self.config.get_bindings().items():
            queues = bindings.queues or {}
            for queue_name in queues.keys():
                await self.teardown_queue_binding(channel, queue_name, exchange)

    async def teardown_queue_binding(self, channel: aio_pika.Channel, queue_name: str, exchange: str):
        exchange_name = self.make_exchange_name(exchange)
        await self.queues[queue_name].unbind(exchange_name)
        self.log.debug(f"Unbound queue {queue_name} from {exchange_name}")

    async def setup_resource_pathways(self, channel: aio_pika.Channel):
        for name, c in self.config.get_resources().items():
            pathways = c.default_pathways or {}
            for pathway, exchanges in pathways.items():
                await self.setup_resource_pathway(channel, name, pathway, exchanges)

    async def setup_resource_pathway(self, channel: aio_pika.Channel, resource_name: str, pathway_name: str, exchanges: List[str]):
        source_exchange_name = self.make_resource_pathway_name(resource_name, pathway_name)
        pathway = await channel.declare_exchange(source_exchange_name, aio_pika.ExchangeType.FANOUT, durable=True)
        self.resource_pathways.setdefault(resource_name, {})
        self.resource_pathways[resource_name][pathway_name] = {
            'pathway': pathway,
            'exchanges': exchanges,
        }
        for name in exchanges:
            exchange_name = self.make_exchange_name(name)
            await self.exchanges[name].bind(source_exchange_name)
            self.log.debug(f"Bound queue {exchange_name} to {source_exchange_name}")

    async def teardown_resource_pathways(self, channel: aio_pika.Channel):
        for pathways in self.resource_pathways.values():
            for pathway_data in pathways.values():
                await self.teardown_resource_pathway(channel, pathway_data)

    async def teardown_resource_pathway(self, channel: aio_pika.Channel, pathway_data: Dict[str, Union[aio_pika.Exchange, List[str]]]):
        pathway = pathway_data['pathway']
        for exchange_name in pathway_data['exchanges']:
            await self.exchanges[exchange_name].unbind(pathway.name)
            self.log.debug(f"Unbound {pathway.name} from {self.exchanges[exchange_name].name}")
        await pathway.delete()
        self.log.debug(f"Removed {pathway.name}")
