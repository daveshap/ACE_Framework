import discord
from discord import Embed

from channels.communication_channel import CommunicationChannel
from filters.image_filter import split_message_by_images
from llm.gpt import GptMessage


class DiscordCommunicationChannel(CommunicationChannel):

    def __init__(self, discord_client, discord_channel, incoming_discord_message, image_generator_function):
        self.discord_client = discord_client
        self.discord_channel = discord_channel
        self.incoming_discord_message = incoming_discord_message
        self.image_generator_function = image_generator_function
        self.response = None

    async def send_message(self, text):
        print("DiscordCommunicationChannel.send_message: " + text)
        segments = await split_message_by_images(self.image_generator_function, text)
        for segment in segments:
            if segment.startswith("http"):
                embed = Embed()
                embed.set_image(url=segment)
                await self.discord_channel.send(embed=embed)
            else:
                await self.discord_channel.send(segment)

    async def get_message_history(self, message_count) -> [GptMessage]:
        conversation: [GptMessage] = []
        discord_messages = await self.get_previous_discord_messages_in_channel(message_count)
        for discord_message in discord_messages:
            conversation.append(self.construct_gpt_message(discord_message))
        conversation.append(self.construct_gpt_message(self.incoming_discord_message))  # appending the incoming message
        return conversation

    async def get_previous_discord_messages_in_channel(self, message_count):
        messages = []
        async for historic_message in self.incoming_discord_message.channel.history(limit=message_count + 1):
            if historic_message.id != self.incoming_discord_message.id:  # skip the triggering message
                messages.append(historic_message)
        return messages[::-1]  # reverse the list, so we get oldest first

    def construct_gpt_message(self, discord_message) -> GptMessage:
        if discord_message.author == self.discord_client.user:
            role = 'assistant'
        else:
            role = 'user'
        name = self.get_user_display_name(discord_message)
        return {"role": role, "name": name, "content": discord_message.content}

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
