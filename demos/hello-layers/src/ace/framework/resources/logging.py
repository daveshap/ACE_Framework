import os
import aio_pika
import yaml

from ace.settings import Settings
from ace.framework.resource import Resource


class LoggingSettings(Settings):
    pass


class Logging(Resource):

    @property
    def settings(self):
        return LoggingSettings(
            name="logging",
            label="Logging",
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    async def post_connect(self):
        await self.subscribe_logging()

    async def pre_disconnect(self):
        await self.unsubscribe_logging()

    async def message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = message.body.decode()
        self.log.debug(f"[{self.labeled_name}] received a message: {body}")
        try:
            data = yaml.safe_load(body)
        except yaml.YAMLError as e:
            self.log.error(f"[{self.labeled_name}] could not parse message: {e}")
            return
        self.log_message(data)

    async def subscribe_logging(self):
        self.log.debug(f"{self.labeled_name} subscribing to logging queue...")
        queue_name = self.settings.logging_queue
        self.consumers[queue_name] = await self.try_queue_subscribe(queue_name, self.message_handler)
        self.log.info(f"{self.labeled_name} subscribed to logging queue")

    async def unsubscribe_logging(self):
        queue_name = self.settings.logging_queue
        if queue_name in self.consumers:
            queue, consumer_tag = self.consumers[queue_name]
            self.log.debug(f"{self.labeled_name} unsubscribing from logging queue...")
            await queue.cancel(consumer_tag)
            self.log.info(f"{self.labeled_name} unsubscribed from logging queue")

    def log_message(self, data):
        self.executor.submit(self._write_log, data)

    def _write_log(self, data):
        timestamp = data.get('timestamp', 'unknown')
        message_type = data.get('type', 'unknown')
        resource = data.get('resource', {})
        source = resource.get('source', 'unknown')
        destination = resource.get('destination', 'unknown')
        message = data.get('message', '')
        filename = f"{source}.{destination}.log"
        filepath = os.path.join(self.settings.log_dir, filename)
        os.makedirs(self.settings.log_dir, exist_ok=True)
        with open(filepath, 'a') as f:
            f.write(f"{timestamp}: ({message_type}) {source} -> {destination}: {message}\n")
