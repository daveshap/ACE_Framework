from ace.types import ChatMessage
from channels.communication_channel import CommunicationChannel


class WebCommunicationChannel(CommunicationChannel):

    def __init__(self, messages: [ChatMessage]):
        self.messages: [ChatMessage] = messages
        self.response = None

    async def send_message(self, text):
        print("WebCommunicationChannel.send_message: " + text)
        self.response = text

    async def get_message_history(self, message_count) -> [ChatMessage]:
        return self.messages

    def describe(self):
        return "Web"
