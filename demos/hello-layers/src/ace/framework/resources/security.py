import logging
import aio_pika

from ace.settings import Settings
from ace.framework.resource import Resource

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SecuritySettings(Settings):
    pass


class Security(Resource):

    @property
    def settings(self):
        return SecuritySettings(
            name="security",
            label="Security",
        )

    # TODO: Add valid status checks.
    def status(self):
        logger.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    async def post_connect(self):
        await self.subscribe_security_queue()
        await self.post_layers()

    async def pre_disconnect(self):
        await self.unsubscribe_security_queue()

    async def publish_message(self, queue_name, message, delivery_mode=2):
        message = aio_pika.Message(
            body=message,
            delivery_mode=delivery_mode
        )
        await self.channel.default_exchange.publish(message, routing_key=queue_name)

    async def post_layers(self):
        for queue_name in self.build_all_layer_queue_names():
            await self.post_layer(queue_name)

    async def post_layer(self, queue_name):
        logger.debug(f"[{self.labeled_name}] sending POST to layer queue: {queue_name}")
        message = self.build_message(message_type='ping')
        await self.publish_message(queue_name, message)

    async def message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            logger.debug(f"[{self.labeled_name}] received a message: {message.body.decode()}")

    async def subscribe_security_queue(self):
        logger.debug(f"{self.labeled_name} subscribing to security queue...")
        queue_name = self.settings.system_integrity_queue
        self.consumers[queue_name] = await self.try_queue_subscribe(queue_name, self.message_handler)
        logger.info(f"{self.labeled_name} Subscribed to security queue")

    async def unsubscribe_security_queue(self):
        logger.debug(f"{self.labeled_name} unsubscribing from security queue...")
        queue_name = self.settings.system_integrity_queue
        await self.consumers[queue_name].cancel()
        logger.info(f"{self.labeled_name} Unsubscribed from security queue")
