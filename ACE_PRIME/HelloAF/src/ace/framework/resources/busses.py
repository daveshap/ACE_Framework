from ace.settings import Settings
from ace.framework.resource import Resource


class BussesSettings(Settings):
    pass


class Busses(Resource):
    @property
    def settings(self):
        return BussesSettings(
            name="busses",
            label="Busses",
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    async def post_connect(self):
        await self.setup_messaging()

    async def pre_disconnect(self):
        await self.teardown_messaging()

    async def setup_messaging(self):
        await self.messaging_config.setup_all(self.consumer_channel)

    async def teardown_messaging(self):
        await self.messaging_config.teardown_all(self.consumer_channel)
