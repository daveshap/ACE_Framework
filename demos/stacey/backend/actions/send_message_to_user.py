from actions.action import Action
from channels.communication_channel import CommunicationChannel


class SendMessageToUser(Action):
    def __init__(self, communication_channel: CommunicationChannel, response_text: str):
        self.communication_channel = communication_channel
        self.response_text = response_text

    async def execute(self):
        print("Executing " + str(self))
        await self.communication_channel.send_message(self.response_text)

    def __str__(self):
        return "send_message_to_user with text: " + self.response_text



