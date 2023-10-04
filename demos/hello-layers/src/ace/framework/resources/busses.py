from ace.settings import Settings
from ace.amqp.exchange import setup_exchange, teardown_exchange
from ace.framework.resource import Resource


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
        # TODO: Need this?
        # await self.create_security_queues()
        await self.create_exchanges()

    async def pre_disconnect(self):
        await self.destroy_exchanges()
        # TODO: Need this?
        # await self.destroy_security_queues()

    async def create_exchanges(self):
        self.log.debug(f"{self.labeled_name} creating exchanges...")
        for queue_name in self.build_all_layer_queue_names():
            await self.create_exchange(queue_name)
        self.log.debug(f"{self.labeled_name} queues created")

    async def create_exchange(self, queue_name):
        await setup_exchange(
            settings=self.settings,
            channel=self.channel,
            queue_name=queue_name,
        )
        self.log.info(f" Created exchange for {queue_name} for resource {self.labeled_name}")

    async def destroy_exchanges(self):
        self.log.debug(f"{self.labeled_name} destroying exchanges...")
        for queue_name in self.build_all_layer_queue_names():
            await self.destroy_exchange(queue_name)
        self.log.debug(f"{self.labeled_name} exchanges destroyed")

    async def destroy_exchange(self, queue_name):
        await teardown_exchange(
            settings=self.settings,
            channel=self.channel,
            queue_name=queue_name,
        )
        self.log.info(f" Destroyed exchange for {queue_name} for resource {self.labeled_name}")

    # TODO: Need this?
    async def create_security_queues(self):
        for layer in self.settings.layers:
            queue_name = f"security.{layer}"
            await self.channel.declare_queue(queue_name, durable=True)

    # TODO: Need this?
    async def destroy_security_queues(self):
        for layer in self.settings.layers:
            queue_name = f"security.{layer}"
            await self.channel.queue_delete(queue_name)
