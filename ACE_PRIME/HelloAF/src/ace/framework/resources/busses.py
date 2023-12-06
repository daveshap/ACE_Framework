from ace.settings import Settings
from ace.framework.resource import Resource
from ace.amqp.config_parser import ConfigParser
from ace.amqp.connection import AMQPConnectionManager
from ace.amqp.setup import AMQPSetupManager


class BussesSettings(Settings):
    pass


class Busses(Resource):

    @property
    def settings(self):
        return BussesSettings(
            name="busses",
            label="Busses",
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    async def post_connect(self):
        await self.setup_connection()
        await self.setup_config_parser()
        await self.setup_messaging()

    async def pre_disconnect(self):
        await self.teardown_messaging()
        await self.teardown_connection()

    async def setup_connection(self):
        self.connection = await self.connection_manager.get_connection(loop=self.bus_loop)
        self.channel = await self.connection.channel()

    async def setup_config_parser(self):
        self.config_parser = ConfigParser()
        self.setup = AMQPSetupManager(self.config_parser)

    async def setup_messaging(self):
        await self.setup.setup_exchanges(self.channel)
        await self.setup.setup_queues(self.channel)
        await self.setup.setup_queue_bindings(self.channel)
        await self.setup.setup_resource_pathways(self.channel)

    async def teardown_messaging(self):
        await self.setup.teardown_resource_pathways(self.channel)
        await self.setup.teardown_queue_bindings(self.channel)
        await self.setup.teardown_queues(self.channel)
        await self.setup.teardown_exchanges(self.channel)

    async def teardown_connection(self):
        await self.channel.close()
        await self.connection.close()
