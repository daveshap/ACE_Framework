import os
import importlib
import fnmatch
from aio_pika import ExchangeType

from ace import util
from ace.settings import Settings
from ace.framework.resource import Resource


class TelemetrySettings(Settings):
    pass


class TelemetryManager(Resource):

    def __init__(self, rabbitmq_server):
        super().__init__()
        self.load_telemetry()

    @property
    def settings(self):
        return TelemetrySettings(
            name="telemetry",
            label="Telemetry",
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    def load_telemetry(self):
        self.telemetry = {}
        self.namespace_map = {}
        # Load Telemetry classes
        package_path = util.get_package_root(self)
        for file in os.listdir(os.path.join(package_path, 'ace', 'framework', 'telemetry')):
            if file.startswith('telemetry_') and file.endswith('.py'):
                name = os.path.splitext(file)[0]
                class_name = util.snake_to_class(name)
                try:
                    module = importlib.import_module(f'ace.framework.telemetry.{name}')
                    class_ = getattr(module, class_name)
                    instance = class_()
                    self.telemetry[name] = instance
                    self.log.info(f"Loaded Telemetry class: {class_name}")
                    for namespace in instance.get_namespaces():
                        self.namespace_map[namespace] = instance
                except Exception as e:
                    self.log.error(f"Failed to load Telemetry class {class_name}, {e}", exc_info=True)
                    raise

    def namespace_root(namespace):
        return namespace.split('.')[0]

    def build_telemetry_message(self, namespace, data):
        root = self.namespace_root(namespace)
        message = self.build_message(root, message=data, message_type='telemetry')
        return message

    async def publish(self, namespace, data):
        try:
            self.log.debug(f"Publishing telemetry data to: {namespace}")
            root = self.namespace_root(namespace)
            exchange = await self.publisher_channel.declare_exchange(root, ExchangeType.TOPIC)
            message = self.build_telemetry_message(namespace, data)
            await exchange.publish(message, routing_key=namespace)
            self.log.debug(f"Published telemetry data to: {namespace}")
        except Exception as e:
            self.log.error(f"Failed to publish telemetry data {namespace}: {e}", exc_info=True)
            raise

    async def subscribe(self, queue_name, namespace):
        root = self.namespace_root(namespace)
        try:
            queue = await self.channel.declare_queue(queue_name)
            await queue.bind(root)
            namespaces = [ns for ns in self.namespace_map if fnmatch.fnmatch(ns, namespace)]
            for namespace in namespaces:
                telemetry = self.namespace_map[namespace]
                data = telemetry.get_data(namespace)
                message = self.build_telemetry_message(namespace, data)
                await queue.publish(message, routing_key=namespace)
            self.log.info(f"Subscribed to telemetry namespace: {namespace}")
        except Exception as e:
            self.log.error(f"Failed to subscribe to telemetry namespace {namespace}: {e}", exc_info=True)
            raise

    async def unsubscribe(self, queue_name, namespace):
        try:
            queue = await self.channel.declare_queue(queue_name)
            await queue.unbind(namespace)
            self.log.info(f"Unsubscribed from telemetry namespace: {namespace}")
        except Exception as e:
            self.log.error(f"Failed to unsubscribe from telemetry namespace {namespace}: {e}", exc_info=True)
            raise
