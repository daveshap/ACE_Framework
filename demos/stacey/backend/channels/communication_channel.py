from abc import ABC, abstractmethod

from llm.gpt import GptMessage


class CommunicationChannel(ABC):

    @abstractmethod
    async def send_message(self, text):
        pass

    @abstractmethod
    async def get_message_history(self, message_count) -> [GptMessage]:
        """ oldest message first """
        pass

    @abstractmethod
    def describe(self):
        pass
