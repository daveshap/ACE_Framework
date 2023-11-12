from abc import ABC, abstractmethod

from ace.types import ChatMessage


class CommunicationChannel(ABC):

    @abstractmethod
    async def send_message(self, text):
        pass

    @abstractmethod
    async def get_message_history(self, message_count) -> [ChatMessage]:
        """ oldest message first """
        pass

    @abstractmethod
    def describe(self):
        pass
