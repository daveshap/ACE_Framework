from actions.action import Action
from channels.communication_channel import CommunicationChannel


class EnrollClient(Action):
    def __init__(self, l2_global_strategy_layer, client_name: str, communication_channel: CommunicationChannel):
        self.l2_global_strategy_layer = l2_global_strategy_layer
        self.client_name = client_name
        self.communication_channel = communication_channel

    async def execute(self):
        await self.l2_global_strategy_layer.enroll_client(self.client_name, self.communication_channel)

    def __str__(self):
        return "Enroll client " + self.client_name



