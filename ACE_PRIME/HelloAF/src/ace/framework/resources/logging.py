import os
import glob
import aio_pika
import yaml

from ace.settings import Settings
from ace.framework.resource import Resource


class LoggingSettings(Settings):
    clear_logs_on_start: bool = True


class Logging(Resource):

    def __init__(self):
        super().__init__()
        if self.settings.clear_logs_on_start:
            self.clear_logs()

    @property
    def settings(self):
        return LoggingSettings(
            name="logging",
            label="Logging",
        )

    def clear_logs(self):
        self.log.info(f"{self.labeled_name} clearing old logs...")
        files = glob.glob(self.settings.log_dir + '/*.log')
        for f in files:
            try:
                os.remove(f)
                self.log.debug(f'{self.labeled_name} file {f} has been removed successfully')
            except OSError as e:
                self.log.error(f'{self.labeled_name} error removing log file: {f} : {e}', exc_info=True)

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    async def message_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = message.body.decode()
        self.log.debug(f"[{self.labeled_name}] received a message: {body}")
        try:
            data = yaml.safe_load(body)
        except yaml.YAMLError as e:
            self.log.error(f"[{self.labeled_name}] could not parse message: {e}", exc_info=True)
            return
        self.log_message(data)

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
