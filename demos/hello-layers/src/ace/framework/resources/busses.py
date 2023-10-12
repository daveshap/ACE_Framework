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
        await self.create_system_integrity_queues()
        await self.create_logging_queues()
        await self.create_exchanges()
        await self.create_telemetry_queues()
        await super().post_connect()

    async def pre_disconnect(self):
        await super().pre_disconnect()
        await self.destroy_exchanges()
        await self.destroy_system_integrity_queues()
        await self.destroy_logging_queues()
        await self.destroy_telemetry_queues()

    async def create_exchanges(self):
        self.log.debug(f"{self.labeled_name} creating exchanges...")
        for queue_name in self.build_all_layer_queue_names():
            await self.create_exchange(queue_name)
        self.log.debug(f"{self.labeled_name} queues created")

    async def create_exchange(self, queue_name, durable=True):
        await setup_exchange(
            settings=self.settings,
            channel=self.publisher_channel,
            queue_name=queue_name,
            durable=durable,
        )
        self.log.info(f" Created exchange for {queue_name} for resource {self.labeled_name}")

    async def destroy_exchanges(self):
        self.log.debug(f"{self.labeled_name} destroying exchanges...")
        for queue_name in self.build_all_layer_queue_names():
            await self.destroy_exchange(queue_name)
        self.log.debug(f"{self.labeled_name} exchanges destroyed")

    async def destroy_exchange(self, queue_name, durable=True):
        await teardown_exchange(
            settings=self.settings,
            channel=self.publisher_channel,
            queue_name=queue_name,
            durable=durable,
        )
        self.log.info(f" Destroyed exchange for {queue_name} for resource {self.labeled_name}")

    async def create_system_integrity_queues(self):
        for layer in self.settings.layers:
            queue_name = self.build_system_integrity_queue_name(layer)
            await self.consumer_channel.declare_queue(queue_name, durable=True)
        for resource in self.settings.other_resources:
            queue_name = self.build_system_integrity_queue_name(resource)
            await self.consumer_channel.declare_queue(queue_name, durable=True)
        await self.create_exchange(self.settings.system_integrity_data_queue, durable=False)

    async def destroy_system_integrity_queues(self):
        for layer in self.settings.layers:
            queue_name = self.build_system_integrity_queue_name(layer)
            await self.consumer_channel.queue_delete(queue_name)
        for resource in self.settings.other_resources:
            queue_name = self.build_system_integrity_queue_name(resource)
            await self.consumer_channel.queue_delete(queue_name)
        await self.destroy_exchange(self.settings.system_integrity_data_queue, durable=False)

    async def create_logging_queues(self):
        await self.create_exchange(self.settings.resource_log_queue)

    async def destroy_logging_queues(self):
        await self.destroy_exchange(self.settings.resource_log_queue)

    async def create_telemetry_queues(self):
        for layer in self.settings.layers:
            queue_name = self.build_telemetry_queue_name(layer)
            await self.consumer_channel.declare_queue(queue_name, durable=True)
        await self.create_exchange(self.settings.telemetry_subscribe_queue)

    async def destroy_telemetry_queues(self):
        for layer in self.settings.layers:
            queue_name = self.build_telemetry_queue_name(layer)
            await self.consumer_channel.queue_delete(queue_name)
        await self.destroy_exchange(self.settings.telemetry_subscribe_queue)
