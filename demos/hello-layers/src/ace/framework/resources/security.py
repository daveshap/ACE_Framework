import logging
import pika

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

    def start_resource(self):
        super().start_resource()
        self.subscribe_all_layers()

    def stop_resource(self):
        self.unsubscribe_all_layers()
        super().stop_resource()

    def send_message(self, layer, message, delivery_mode=2):
        queue_name = f"security.{layer}"
        self.publish_message(self, queue_name, message)

    def publish_message(self, queue, message, delivery_mode=2):
        self.channel.basic_publish(exchange='',
                                   routing_key=queue,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=delivery_mode,
                                   ))

    def post(self):
        for layer in self.settings.layers:
            self.post_layer(layer)

    def post_layer(self, layer):
        self.logger.debug(f"[{self.labeled_name}] sending POST to layer: {layer}")
        message = self.build_message(message_type='ping')
        self.send_message(self, layer, message)

    def message_handler(self, channel: pika.channel.Channel, method: pika.spec.Basic.Deliver, properties: pika.spec.BasicProperties, body: bytes):
        logger.debug(f"[{self.labeled_name}] received a message: {body.decode()}")

    def subscribe_all_layers(self):
        logger.debug(f"{self.labeled_name} subscribing to all layers...")
        for queue_name in self.build_all_layer_queue_names():
            # TODO: Consider separate message handlers?
            self.try_queue_subscribe(queue_name, self.message_handler)
        logger.info(f"{self.labeled_name} Subscribed to all layers")

    def unsubscribe_all_layers(self):
        logger.debug(f"{self.labeled_name} unsubscribing from all layers...")
        for queue_name in self.build_all_layer_queue_names():
            self.channel.basic_cancel(queue_name)
        logger.info(f"{self.labeled_name} Unsubscribed from all layers")
