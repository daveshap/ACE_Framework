import asyncio

from dotenv import load_dotenv

from ace.ace_system import AceSystem
from channels.web.fastapi_app import FastApiApp
from llm.gpt import GPT
from media.giphy_finder import GiphyFinder
from util import get_environment_variable


async def main():
    load_dotenv()
    openai_api_key = get_environment_variable('OPENAI_API_KEY')
    llm = GPT(openai_api_key)
    giphy = GiphyFinder(get_environment_variable('GIPHY_API_KEY'))
    media_generators = [
        {"keyword": "IMAGE", "generator_function": llm.create_image},
        {"keyword": "GIF", "generator_function": giphy.get_giphy_url}
    ]
    ace = AceSystem(llm, get_environment_variable("DEFAULT_MODEL"))
    await ace.start()
    fastapi_app = FastApiApp(ace, media_generators)
    await fastapi_app.run()  # Now you can use await here

if __name__ == "__main__":
    asyncio.run(main())
