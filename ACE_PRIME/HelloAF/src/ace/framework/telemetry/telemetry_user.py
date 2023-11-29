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
        signal.signal(signal.SIGUSR1, self.schedule_receive_event)

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

    def schedule_receive_event(self, signal, frame):
        self.log.info(f"{self.labeled_name} received SIGUSR1 signal")
        loop = asyncio.get_event_loop()
        loop.call_soon_threadsafe(loop.create_task, self.receive_encouragement_event())

    async def receive_encouragement_event(self):
        self.log.info(f"{self.labeled_name} add some encouragement...")
        await self.collection_event('user.encouragement')
