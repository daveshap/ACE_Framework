import os
import discord
from dotenv import load_dotenv
import gpt
import config
import pprint

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
        print(pprint.pformat(message.author))

        # Initialize conversation with the system message
        conversation = [{"role": "system", "content": config.system_message}]

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
            print(f"  Sending conversation to GPT-3: {pprint.pformat(conversation)}")
            response = gpt.create_chat_completion('gpt-3.5-turbo', conversation)
            print(f"  Responding to {message.author}: {response['content']}")
            await message.channel.send(response['content'])
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
    client.run(os.getenv("DISCORD_BOT_TOKEN"))


if __name__ == '__main__':
    run()
