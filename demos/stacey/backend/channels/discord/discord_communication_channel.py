import discord
from discord import Embed

from ace.types import ChatMessage
from channels.communication_channel import CommunicationChannel
from media.media_replace import MediaGenerator, split_message_by_media


class DiscordCommunicationChannel(CommunicationChannel):

    def __init__(self, discord_client, discord_channel, incoming_discord_message, media_generators: [MediaGenerator]):
        self.discord_client = discord_client
        self.discord_channel = discord_channel
        self.incoming_discord_message = incoming_discord_message
        self.media_generators = media_generators
        self.response = None

    async def send_message(self, text):
        print("DiscordCommunicationChannel.send_message: " + text)
        segments = await split_message_by_media(self.media_generators, text)
        print("Segments: " + str(segments))
        for segment in segments:
            if segment.startswith("http"):
                embed = Embed()
                embed.set_image(url=segment)
                await self.discord_channel.send(embed=embed)
            else:
                await self.discord_channel.send(segment)

    async def get_message_history(self, message_count) -> [ChatMessage]:
        chat_messages: [ChatMessage] = []
        discord_messages = await self.get_previous_discord_messages_in_channel(message_count)
        for discord_message in discord_messages:
            chat_messages.append(self.construct_chat_message(discord_message))
        chat_messages.append(self.construct_chat_message(self.incoming_discord_message))
        return chat_messages

    async def get_previous_discord_messages_in_channel(self, message_count):
        messages = []
        async for historic_message in self.incoming_discord_message.channel.history(limit=message_count + 1):
            if historic_message.id != self.incoming_discord_message.id:  # skip the triggering message
                messages.append(historic_message)
        return messages[::-1]  # reverse the list, so we get oldest first

    def construct_chat_message(self, discord_message) -> ChatMessage:
        name = self.get_user_display_name(discord_message)
        return ChatMessage(sender=name, content=discord_message.content, time_utc=discord_message.created_at)

    @staticmethod
    def get_user_display_name(msg):
        if isinstance(msg.author, discord.Member):
            if msg.author.nick:
                return msg.author.nick
        if hasattr(msg.author, 'global_name') and getattr(msg.author, 'global_name'):
            return getattr(msg.author, 'global_name')
        return msg.author.name

    def describe(self):
        return "Discord"
