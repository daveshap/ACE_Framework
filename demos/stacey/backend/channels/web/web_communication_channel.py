from ace.types import ChatMessage, create_chat_message
from channels.communication_channel import CommunicationChannel
from channels.web.web_socket_connection_manager import WebSocketConnectionManager
from media.media_replace import replace_media_prompt_with_media_url_formatted_as_markdown, MediaGenerator


class WebCommunicationChannel(CommunicationChannel):

    def __init__(self, messages: [ChatMessage],
                 web_socket: WebSocketConnectionManager, media_generators: [MediaGenerator]):
        self.messages: [ChatMessage] = messages
        self.web_socket = web_socket
        self.media_generators = media_generators

    async def send_message(self, text):
        print("WebCommunicationChannel.send_message: " + text)
        response_with_images = await replace_media_prompt_with_media_url_formatted_as_markdown(
            self.media_generators, text
        )
        chat_message = create_chat_message("Stacey", response_with_images)
        await self.web_socket.send_message(chat_message)
        print("WebCommunicationChannel sent message!")

    async def get_message_history(self, message_count) -> [ChatMessage]:
        return self.messages

    def describe(self):
        return "Web"
