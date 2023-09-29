import multiprocessing
import os

import flask_app
import discord_bot
from dotenv import load_dotenv
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
