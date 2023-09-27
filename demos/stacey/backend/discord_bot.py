import os
import discord
from dotenv import load_dotenv
import gpt
import config

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in to discord as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'stacey' in message.content.lower():
        print(f"Got discord message from {message.author}: {message.content}")

        conversation = [
            {"role": "system", "content": config.system_message},
            {"role": "user", "content": message.content}  # User's message
        ]

        try:
            response = gpt.create_chat_completion('gpt-3.5-turbo', conversation)

            print(f"  Responding to {message.author}: {response['content']}")
            await message.channel.send(response['content'])
        except Exception as e:
            await message.channel.send(f"Damn! Something went wrong!: {str(e)}")


def run():
    client.run(os.getenv("DISCORD_BOT_TOKEN"))


if __name__ == '__main__':
    run()
