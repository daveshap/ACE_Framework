from channels.communication_channel import CommunicationChannel
from llm.gpt import GptMessage


class WebCommunicationChannel(CommunicationChannel):

    def __init__(self, conversation: [GptMessage]):
        self.conversation = conversation
        self.response = None

    async def send_message(self, text):
        print("WebCommunicationChannel.send_message: " + text)
        self.response = text

    async def get_message_history(self, message_count):
        return self.conversation

    def describe(self):
        return "Web"
