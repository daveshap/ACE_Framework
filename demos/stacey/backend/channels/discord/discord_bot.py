# channels/discord/discord_bot.py
import pprint
import traceback

import discord

from ace.ace_system import AceSystem
from channels.discord.discord_communication_channel import DiscordCommunicationChannel
from media.media_replace import MediaGenerator


class DiscordBot:
    def __init__(self, bot_token, bot_name, ace_system: AceSystem, media_generators: [MediaGenerator]):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.bot_token = bot_token
        self.bot_name = bot_name.lower()
        self.register_events()
        self.ace_system = ace_system
        self.media_generators = media_generators

    def register_events(self):
        @self.client.event
        async def on_ready():
            print(f'We have logged in to discord as {self.client.user}')

        @self.client.event
        async def on_message(message):
            await self.process_message(message)

    async def process_message(self, message):
        # Check if the message is from an allowed channel
        if message.channel.name not in ["bot-testing", "team5-stacey", "chat1"]:
            return

        if self.is_message_from_me(message):
            return

        print(f"Got discord message from {message.author}: {message.content}")
        print(pprint.pformat(message.author))

        discord_communication_channel = DiscordCommunicationChannel(
            self.client, message.channel, message, self.media_generators
        )

        try:
            await self.ace_system.l3_agent.process_incoming_user_message(discord_communication_channel)
        except Exception as e:
            print("Damn! Something went wrong!", e)
            traceback_str = traceback.format_exc()  # Get the string representation of the traceback
            print("Traceback:", traceback_str)
            await message.channel.send(f"Damn! Something went wrong!: {str(e)}")

    def is_message_from_me(self, message):
        return message.author == self.client.user

    def run(self):
        """ NOTE: this is a blocking call """
        self.client.run(self.bot_token)
