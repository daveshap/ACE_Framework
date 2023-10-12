import asyncio

from dotenv import load_dotenv

from ace.ace_system import AceSystem
from channels.discord.discord_bot import DiscordBot
from channels.web.fastapi_app import FastApiApp
from llm.gpt import GPT
from media.giphy_finder import GiphyFinder
from memory.weaviate_memory_manager import WeaviateMemoryManager
from util import get_environment_variable


async def stacey_main(start_discord, start_web):
    load_dotenv()
    openai_api_key = get_environment_variable('OPENAI_API_KEY')
    llm = GPT(openai_api_key)
    weaviate_url = get_environment_variable('WEAVIATE_URL')
    memory_manager = WeaviateMemoryManager(weaviate_url, openai_api_key)
    ace = AceSystem(llm, get_environment_variable("DEFAULT_MODEL"), memory_manager)

    giphy = GiphyFinder(get_environment_variable('GIPHY_API_KEY'))
    media_generators = [
        {"keyword": "IMAGE", "generator_function": llm.create_image},
        {"keyword": "GIF", "generator_function": giphy.get_giphy_url}
    ]

    await ace.start()

    discord_task = asyncio.create_task(asyncio.sleep(0))
    if start_discord:
        discord_bot_token = get_environment_variable('DISCORD_BOT_TOKEN')
        discord_bot = DiscordBot(discord_bot_token, "stacey", ace, media_generators)
        print('Starting discord bot')
        discord_task = asyncio.create_task(discord_bot.start())
        print('Started discord bot')

    web_task = asyncio.create_task(asyncio.sleep(0))
    if start_web:
        web_backend = FastApiApp(ace, media_generators, llm)
        print('Starting web backend')
        web_task = asyncio.create_task(web_backend.run())
        print('Started web backend')

    await asyncio.gather(discord_task, web_task)

if __name__ == '__main__':
    asyncio.run(stacey_main(start_discord=True, start_web=True))
