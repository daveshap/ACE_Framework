import os
import yaml
import importlib
import fnmatch
import asyncio
import aio_pika

from ace import util
from ace.settings import Settings
from ace.framework.resource import Resource
from ace.amqp.setup import ExchangeConfig


class TelemetrySettings(Settings):
    pass


class TelemetryManager(Resource):
    def __init__(self):
        super().__init__()
        self.load_telemetry()
        self.exchanges = {k: False for k in self.unique_roots()}

    def setup_service(self):
        self.initial_collection()
        super().setup_service()

    def post_start(self):
        self.schedule_collecting()

    def pre_stop(self):
        self.stop_collecting()

    async def post_connect(self):
        await self.make_exchanges()

    async def pre_disconnect(self):
        await self.teardown_messaging()

    def initial_collection(self):
        asyncio.run_coroutine_threadsafe(
            self.collect_initial_data_points(), self.bus_loop
        )

    def schedule_collecting(self):
        self.log.info(
            f"{self.labeled_name} scheduling recurring data points collection"
        )
        for namespace, telemetry in self.namespace_map.items():
            telemetry.start_collecting(namespace)
        self.log.info(
            f"{self.labeled_name} finished scheduling recurring data points collection"
        )

    def stop_collecting(self):
        self.log.info(f"{self.labeled_name} stopping recurring data points collection")
        for namespace, telemetry in self.namespace_map.items():
            telemetry.stop_collecting(namespace)
        self.log.info(
            f"{self.labeled_name} finished stopping recurring data points collection"
        )

    @property
    def settings(self):
        return TelemetrySettings(
            name="telemetry_manager",
            label="Telemetry Manager",
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
        for file in os.listdir(os.path.join(package_path, "framework", "telemetry")):
            if file.startswith("telemetry_") and file.endswith(".py"):
                name = os.path.splitext(file)[0]
                class_name = util.snake_to_class(name)
                self.log.debug(
                    f"{self.labeled_name} found telemetry file {file}: name={name}, class_name={class_name}"
                )
                try:
                    self.log.debug(
                        f"{self.labeled_name} loading Telemetry class: {class_name}"
                    )
                    module = importlib.import_module(f"ace.framework.telemetry.{name}")
                    class_ = getattr(module, class_name)
                    instance = class_(publisher=self.publish)
                    self.telemetry[name] = instance
                    self.log.info(
                        f"{self.labeled_name} loaded Telemetry class: {class_name}"
                    )
                    for namespace in instance.namespaces:
                        self.namespace_map[namespace] = instance
                except Exception as e:
                    self.log.error(
                        f"{self.labeled_name} failed to load Telemetry class {class_name}, {e}",
                        exc_info=True,
                    )
                    raise

    def build_telemetry_exchange_name(self, root):
        return f"telemetry.{root}"

    def unique_roots(self):
        return list(set(self.namespace_root(key) for key in self.namespace_map.keys()))

    def namespace_root(self, namespace):
        return namespace.split(".")[0]

    def build_telemetry_message(self, namespace, data):
        root = self.namespace_root(namespace)
        message = self.build_message(
            self.build_telemetry_exchange_name(root),
            message={"namespace": namespace, "data": data},
            message_type="telemetry",
        )
        return message

    async def make_exchanges(self):
        for root in self.unique_roots():
            await self.make_exchange(root)

    async def teardown_messaging(self):
        await self.messaging_config.teardown_exchanges(self.consumer_channel)

    async def make_exchange(self, root):
        exchange_name = self.build_telemetry_exchange_name(root)
        self.exchanges[root] = await self.messaging_config.setup_exchange(
            self.consumer_channel, exchange_name, ExchangeConfig(type="topic")
        )

    async def collect_initial_data_points(self):
        self.log.info(f"{self.labeled_name} starting initial data points collection")
        asyncio.set_event_loop(self.bus_loop)
        tasks = [
            self.bus_loop.create_task(telemetry.collect_data(namespace))
            for namespace, telemetry in self.namespace_map.items()
        ]
        await asyncio.gather(*tasks)
        self.log.info(f"{self.labeled_name} finished initial data points collection")

    async def publish_exchange_message(
        self, exchange, body, routing_key, delivery_mode=2
    ):
        message = aio_pika.Message(body=body, delivery_mode=delivery_mode)
        await exchange.publish(message, routing_key=routing_key)

    async def publish_queue_message(self, queue_name, message, delivery_mode=2):
        message = aio_pika.Message(body=message, delivery_mode=delivery_mode)
        await self.publisher_channel.default_exchange.publish(
            message, routing_key=queue_name
        )

    async def publish(self, namespace, data):
        try:
            self.log.debug(
                f"{self.labeled_name} publishing telemetry data to: {namespace}"
            )
            root = self.namespace_root(namespace)
            exchange = await self.make_exchange(root)
            message = self.build_telemetry_message(namespace, data)
            await self.publish_exchange_message(exchange, message, namespace)
            self.log.debug(
                f"{self.labeled_name} published telemetry data to: {namespace}"
            )
        except Exception as e:
            self.log.error(
                f"{self.labeled_name} failed to publish telemetry data to {namespace}: {e}",
                exc_info=True,
            )
            raise

    async def subscribe(self, queue_name, namespace):
        try:
            self.log.debug(
                f"{self.labeled_name} subscribing queue {queue_name} to telemetry namespace: {namespace}"
            )
            queue = await self.consumer_channel.declare_queue(queue_name, durable=True)
            root = self.namespace_root(namespace)
            exchange = self.exchanges[root]
            while not bool(exchange):
                self.log.debug(
                    f"{self.labeled_name} waiting for telemetry exchange root: {root}..."
                )
                await asyncio.sleep(1)
            await queue.bind(exchange.name, routing_key=namespace)
            namespaces = [
                ns for ns in self.namespace_map if fnmatch.fnmatch(ns, namespace)
            ]
            for ns in namespaces:
                telemetry = self.namespace_map[ns]
                data = await telemetry.get_data(ns)
                message = self.build_telemetry_message(ns, data)
                self.log.debug(
                    f"{self.labeled_name} publishing initial telemetry for namespace {ns} to queue: {queue_name}"
                )
                await self.publish_queue_message(queue_name, message)
            self.log.info(
                f"{self.labeled_name} subscribed queue {queue_name} to telemetry namespace: {namespace}"
            )
        except Exception as e:
            self.log.error(
                f"{self.labeled_name} failed to subscribe queue {queue_name} to telemetry namespace {namespace}: {e}",
                exc_info=True,
            )

    async def unsubscribe(self, queue_name, namespace):
        try:
            self.log.debug(
                f"{self.labeled_name} unsubscribing queue {queue_name} from telemetry namespace: {namespace}"
            )
            queue = await self.consumer_channel.declare_queue(queue_name, durable=True)
            root = self.namespace_root(namespace)
            await queue.unbind(self.exchanges[root].name)
            self.log.info(
                f"{self.labeled_name} unsubscribed queue {queue_name} from telemetry namespace: {namespace}"
            )
        except Exception as e:
            self.log.error(
                f"{self.labeled_name} failed to unsubscribe queue {queue_name} from telemetry namespace {namespace}: {e}",
                exc_info=True,
            )

    async def handle_subscribe_unsubscribe(self, data):
        if data["type"] == "subscribe":
            await self.subscribe(data["queue"], data["namespace"])
        elif data["type"] == "unsubscribe":
            await self.unsubscribe(data["queue"], data["namespace"])

    async def message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = message.body.decode()
        self.log.debug(f"[{self.labeled_name}] received a message: {body}")
        try:
            data = yaml.safe_load(body)
        except yaml.YAMLError as e:
            self.log.error(
                f"[{self.labeled_name}] could not parse message: {e}", exc_info=True
            )
            return
        await self.handle_subscribe_unsubscribe(data)
