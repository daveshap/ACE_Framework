import asyncio
import threading

from dotenv import load_dotenv

from ace.ace_system import AceSystem
from channels.discord.discord_bot import DiscordBot
from channels.web.fastapi_app import FastApiApp
from llm.gpt import GPT
from media.giphy_finder import GiphyFinder
from util import get_environment_variable


def run_discord_bot(discord_bot):
    discord_bot.run()


async def main():
    openai_api_key = get_environment_variable('OPENAI_API_KEY')
    llm = GPT(openai_api_key)
    ace = AceSystem(llm, get_environment_variable("DEFAULT_MODEL"))

    giphy = GiphyFinder(get_environment_variable('GIPHY_API_KEY'))
    media_generators = [
        {"keyword": "IMAGE", "generator_function": llm.create_image},
        {"keyword": "GIF", "generator_function": giphy.get_giphy_url}
    ]

    discord_bot_token = get_environment_variable('DISCORD_BOT_TOKEN')
    discord_bot = DiscordBot(discord_bot_token, "stacey", ace, media_generators)

    # Launch the Discord bot in a separate thread, since discord_bot.run() is blocking
    discord_thread = threading.Thread(target=run_discord_bot, args=(discord_bot,))
    discord_thread.start()

    # Start the Ace system
    await ace.start()

    # Start the web backend
    web_backend = FastApiApp(ace, media_generators)
    await web_backend.run()

if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
