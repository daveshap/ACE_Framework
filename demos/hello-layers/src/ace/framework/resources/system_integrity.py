import aio_pika
import asyncio
import yaml

from ace.settings import Settings
from ace.framework.resource import Resource


class SystemIntegritySettings(Settings):
    pass


class SystemIntegrity(Resource):

    def __init__(self):
        super().__init__()
        self.post_complete = False
        self.post_verification_matrix = self.compute_ping_pong_combinations()

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

    def post_start(self):
        asyncio.set_event_loop(self.bus_loop)
        self.bus_loop.create_task(self.post_layers())

    async def pre_disconnect(self):
        await self.unsubscribe_system_integrity()

    async def publish_message(self, queue_name, message, delivery_mode=2):
        message = aio_pika.Message(
            body=message,
            delivery_mode=delivery_mode
        )
        await self.publisher_channel.default_exchange.publish(message, routing_key=queue_name)

    async def post_layers(self):
        for layer in self.settings.layers:
            await self.post_layer(layer)

    async def post_layer(self, layer):
        self.log.debug(f"[{self.labeled_name}] sending POST command to layer: {layer}")
        queue_name = self.build_system_integrity_queue_name(layer)
        message = self.build_message(layer, message={'method': 'post'}, message_type='command')
        await self.publish_message(queue_name, message)

    async def message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = message.body.decode()
        self.log.debug(f"[{self.labeled_name}] received a message: {body}")
        try:
            data = yaml.safe_load(body)
        except yaml.YAMLError as e:
            self.log.error(f"[{self.labeled_name}] could not parse message: {e}")
            return
        if not self.post_complete:
            self.check_post_complete(data)

    def check_post_complete(self, data):
        if data['type'] in ['ping', 'pong']:
            if self.verify_ping_pong_sequence_complete(f"{data['type']}.{data['resource']['source']}.{data['resource']['destination']}"):
                self.log.info(f"[{self.labeled_name}] verified POST complete for all layers")

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

    def compute_ping_pong_combinations(self):
        layers = self.settings.layers
        combinations = {}
        for i in range(len(layers)):
            # First layer has no northen layer.
            if i != 0:
                combinations[f"ping.{layers[i-1]}.{layers[i]}"] = False
                combinations[f"pong.{layers[i]}.{layers[i-1]}"] = False
            # Last layer has no southern layer.
            if i != len(layers) - 1:
                combinations[f"ping.{layers[i+1]}.{layers[i]}"] = False
                combinations[f"pong.{layers[i]}.{layers[i+1]}"] = False
        return combinations

    def verify_ping_pong_sequence_complete(self, step):
        if step in self.post_verification_matrix:
            self.post_verification_matrix[step] = True
        return all(value for value in self.post_verification_matrix.values())
