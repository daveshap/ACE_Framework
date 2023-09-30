# discord_bot.py
import pprint
import traceback

import discord
from discord import Embed
from dotenv import load_dotenv

import config
from ace.ace_system import AceSystem
from tools.image_tool import split_message_by_images


class DiscordBot:
    def __init__(self, bot_token, bot_name, ace_system: AceSystem, image_generator_function):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.bot_token = bot_token
        self.bot_name = bot_name.lower()
        self.register_events()
        self.ace_system = ace_system
        self.image_generator_function = image_generator_function

    def register_events(self):
        @self.client.event
        async def on_ready():
            print(f'We have logged in to discord as {self.client.user}')

        @self.client.event
        async def on_message(message):
            await self.process_message(message)

    async def process_message(self, message):
        if self.is_message_from_me(message):
            return

        if not self.am_i_mentioned(message):
            return

        print(f"Got discord message from {message.author}: {message.content}")
        print(pprint.pformat(message.author))

        conversation = await self.construct_conversation(message)

        try:
            response = self.get_bot_response(conversation, message)
            if response:
                await self.send_response(response, message)
        except Exception as e:
            print("Damn! Something went wrong!", e)
            traceback_str = traceback.format_exc()  # Get the string representation of the traceback
            print("Traceback:", traceback_str)
            await message.channel.send(f"Damn! Something went wrong!: {str(e)}")

    def is_message_from_me(self, message):
        return message.author == self.client.user

    def am_i_mentioned(self, message):
        return self.bot_name.lower() in message.content.lower()

    async def construct_conversation(self, message):
        conversation = []
        messages = await self.get_previous_discord_messages_in_channel(message)
        for msg in messages:
            conversation.append(self.construct_message(msg))
        conversation.append(self.construct_message(message))  # appending the user's latest message
        return conversation

    async def get_previous_discord_messages_in_channel(self, current_message):
        """
            returns oldest message first
        """
        messages = []
        async for historic_message in current_message.channel.history(limit=config.discord_message_history_count + 1):
            if historic_message.id != current_message.id:  # skip the triggering message
                messages.append(historic_message)
        return messages[::-1]  # reverse the list

    def construct_message(self, message):
        if message.author == self.client.user:
            role = 'assistant'
        else:
            role = 'user'
        name = self.get_user_display_name(message)
        return {"role": role, "name": name, "content": message.content}

    def get_bot_response(self, conversation, message):
        communication_context = f"discord server '{message.guild.name}', channel #{message.channel.name}"

        response = self.ace_system.l3_agent.generate_response(conversation, communication_context)
        if response is None:
            print("The agent layer decided to not respond to this, so I won't write anything on discord.")
        return response

    async def send_response(self, response, message):
        response_content = response['content']
        segments = split_message_by_images(self.image_generator_function, response_content)
        for segment in segments:
            if segment.startswith("http"):
                embed = Embed()
                embed.set_image(url=segment)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(segment)

    @staticmethod
    def get_user_display_name(msg):
        if isinstance(msg.author, discord.Member):
            if msg.author.nick:
                return msg.author.nick
        if hasattr(msg.author, 'global_name') and getattr(msg.author, 'global_name'):
            return getattr(msg.author, 'global_name')
        return msg.author.name

    def run(self):
        self.client.run(self.bot_token)


def main():
    from llm.gpt import GPT
    import os
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')
    llm = GPT(openai_api_key)
    discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')
    ace = AceSystem(llm, config.default_model)
    discord_bot = DiscordBot(discord_bot_token, "stacey", ace, llm.create_image)
    discord_bot.run()


if __name__ == '__main__':
    main()
