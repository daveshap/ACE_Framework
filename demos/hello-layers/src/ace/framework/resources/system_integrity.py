import aio_pika

from ace.settings import Settings
from ace.framework.resource import Resource


class SystemIntegritySettings(Settings):
    pass


class SystemIntegrity(Resource):

    @property
    def settings(self):
        return SystemIntegritySettings(
            name="system_integrity",
            label="System Integrity",
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    async def post_connect(self):
        await self.subscribe_system_integrity()
        await self.post_layers()

    async def pre_disconnect(self):
        await self.unsubscribe_system_integrity()

    async def publish_message(self, queue_name, message, delivery_mode=2):
        message = aio_pika.Message(
            body=message,
            delivery_mode=delivery_mode
        )
        await self.publisher_channel.default_exchange.publish(message, routing_key=queue_name)

    async def post_layers(self):
        for queue_name in self.build_all_layer_queue_names():
            await self.post_layer(queue_name)

    async def post_layer(self, queue_name):
        self.log.debug(f"[{self.labeled_name}] sending POST to layer queue: {queue_name}")
        message = self.build_message(queue_name, message_type='ping')
        await self.publish_message(queue_name, message)

    async def message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            self.log.debug(f"[{self.labeled_name}] received a message: {message.body.decode()}")

    async def subscribe_system_integrity(self):
        self.log.debug(f"{self.labeled_name} subscribing to system integrity queue...")
        queue_name = self.settings.system_integrity_queue
        self.consumers[queue_name] = await self.try_queue_subscribe(queue_name, self.message_handler)
        self.log.info(f"{self.labeled_name} Subscribed to system integrity queue")

    async def unsubscribe_system_integrity(self):
        self.log.debug(f"{self.labeled_name} unsubscribing from system integrity queue...")
        queue_name = self.settings.system_integrity_queue
        await self.consumers[queue_name].cancel()
        self.log.info(f"{self.labeled_name} Unsubscribed from system integrity queue")
