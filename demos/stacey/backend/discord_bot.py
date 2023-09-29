# discord_bot.py
import os
import pprint

import discord
from discord import Embed
from dotenv import load_dotenv

import ace.l3_agent
import config
from llm.gpt import GPT
from response_generator import generate_response
from tools.image_tool import split_message_by_images

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

llm = GPT(os.getenv("OPENAI_API_KEY"))


@client.event
async def on_ready():
    print(f'We have logged in to discord as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'stacey' in message.content.lower():
        print(f"Got discord message from {message.author}: {message.content}")
        print(pprint.pformat(message.author))

        # Initialize conversation with the system message
        conversation = [{"role": "system", "content": ace.l3_agent.system_message}]

        # Fetch message history and append to conversation
        messages = []
        async for msg in message.channel.history(limit=config.discord_message_history_count + 1):  # +1 to include the triggering message
            if msg.id == message.id:  # skip the triggering message
                continue
            messages.append(msg)

        # Ensure messages are in the correct chronological order and append them to the conversation array.
        for msg in reversed(messages):
            role = 'user' if msg.author != client.user else 'assistant'
            name = get_user_display_name(msg)
            if msg.author == client.user:  # if the author is the bot, use 'Stacey' as the name
                name = 'Stacey'
            conversation.append({"role": role, "name": name, "content": msg.content})

        # Append user's latest message
        user_name = get_user_display_name(message)
        conversation.append({"role": "user", "name": user_name, "content": message.content})

        try:
            communication_context = f"discord server '{message.guild.name}', channel #{message.channel.name}"
            response = generate_response(llm, config.default_model, conversation, communication_context)
            if response is None:
                print("GPT decided to not respond to this, so I won't write anything on discord.")
                return

            response_content = response['content']
            segments = split_message_by_images(response_content)  # Split the response_content by images.
            for segment in segments:
                if segment.startswith("http"):  # Check if the segment is an image URL.
                    embed = Embed()  # Create a Discord Embed object.
                    embed.set_image(url=segment)  # Set the image URL in the embed object.
                    await message.channel.send(embed=embed)  # Send the embed containing the image.
                else:
                    await message.channel.send(segment)  # Send the text segment.
        except Exception as e:
            await message.channel.send(f"Damn! Something went wrong!: {str(e)}")


def get_user_display_name(msg):
    # Check if author is a Member object, which means the message is from a server.
    if isinstance(msg.author, discord.Member):
        if msg.author.nick:
            return msg.author.nick

    # Check if global_name attribute exists, if it's a valid custom attribute.
    if hasattr(msg.author, 'global_name') and getattr(msg.author, 'global_name'):
        return getattr(msg.author, 'global_name')

    # Fall back to the name attribute, which exists on both User and Member objects.
    return msg.author.name


def run():
    if os.getenv("DISCORD_BOT_TOKEN") is None:
        print("DISCORD_BOT_TOKEN environment variable isn't set, so I won't connect to discord.")
        return

    client.run(os.getenv("DISCORD_BOT_TOKEN"))


if __name__ == '__main__':
    run()
