from actions.action import Action


class SetNextAlarm(Action):
    def __init__(self, l3_agent_layer, time_utc: str):
        self.l3_agent_layer = l3_agent_layer
        self.time_utc = time_utc

    async def execute(self):
        await self.l3_agent_layer.set_next_alarm(self.time_utc)

    def __str__(self):
        return "Update whiteboard"
