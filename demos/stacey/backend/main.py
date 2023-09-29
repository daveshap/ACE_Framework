import multiprocessing
import os

from dotenv import load_dotenv

import config
import discord_bot
import flask_app
from ace.ace_system import AceSystem
from llm.gpt import GPT

load_dotenv()

if __name__ == '__main__':
    if os.getenv("OPENAI_API_KEY") is None:
        print("OPENAI_API_KEY is not set. Please set that in backend/.env")
        exit(1)

    flask_process = multiprocessing.Process(target=flask_app.run)
    discord_process = multiprocessing.Process(target=discord_bot.run)

    flask_process.start()
    discord_process.start()

    flask_process.join()
    discord_process.join()

    llm = GPT(os.getenv("OPENAI_API_KEY"))
    ace_system = AceSystem(llm, config.default_model)
    ace_system.start()

