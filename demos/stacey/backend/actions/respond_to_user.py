from actions.action import Action
from channels.communication_channel import CommunicationChannel


class RespondToUser(Action):
    def __init__(self, communication_channel: CommunicationChannel, response_text: str):
        self.communication_channel = communication_channel
        self.response_text = response_text

    async def execute(self):
        await self.communication_channel.send_message(self.response_text)



