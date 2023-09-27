import os
import discord
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if 'stacey' in message.content.lower():
        await message.channel.send('Hello! Stacey here.')

client.run(os.getenv("DISCORD_BOT_TOKEN"))