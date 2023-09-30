import os
import threading

from dotenv import load_dotenv

import config
from ace.ace_system import AceSystem
from discord_bot import DiscordBot
from flask_app import FlaskApp
from llm.gpt import GPT

if __name__ == '__main__':
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')
    llm = GPT(openai_api_key)
    ace = AceSystem(llm, config.default_model)
    ace.start()

    flask_app = FlaskApp(ace, llm.create_image)

    discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')
    discord_bot = DiscordBot(discord_bot_token, "stacey", ace, llm.create_image)

    flask_thread = threading.Thread(target=flask_app.run, daemon=True)
    discord_thread = threading.Thread(target=discord_bot.run, daemon=True)

    flask_thread.start()
    discord_thread.start()

    flask_thread.join()
    discord_thread.join()


