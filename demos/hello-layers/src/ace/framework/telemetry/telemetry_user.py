import asyncio
import signal

from ace.framework.telemetry import Telemetry, TelemetrySettings

USER_ENCOURAGEMENT_PHRASE = "You got this!"

ENVIRONMENT_CONSTANTS = {
    'user.encouragement': USER_ENCOURAGEMENT_PHRASE,
}


class TelemetryUser(Telemetry):

    def __init__(self, publisher=None):
        super().__init__(publisher)
        self.loop = asyncio.get_event_loop()
        self.loop.add_signal_handler(signal.SIGUSR1, self.schedule_receive_event)

    @property
    def settings(self):
        return TelemetrySettings(
            name="telemetry_user",
            label="Telemetry - User",
            namespaces={
                'user.encouragement': 0,
            }
        )

    async def collect_data_sample(self, namespace):
        if namespace in ENVIRONMENT_CONSTANTS:
            return ENVIRONMENT_CONSTANTS[namespace]

    def schedule_receive_event(self):
        self.loop.create_task(self.receive_encouragement_event())

    async def receive_encouragement_event(self):
        self.log.info("Received SIGUSR1 signal -- let's add some encouragement...")
        await self.collection_event()

