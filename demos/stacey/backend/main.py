import threading

from dotenv import load_dotenv

from ace.ace_system import AceSystem
from channels.discord.discord_bot import DiscordBot
from channels.web.flask_app import FlaskApp
from llm.gpt import GPT
from util import get_environment_variable

if __name__ == '__main__':
    load_dotenv()
    openai_api_key = get_environment_variable('OPENAI_API_KEY')
    llm = GPT(openai_api_key)
    ace = AceSystem(llm, get_environment_variable("DEFAULT_MODEL"))

    flask_app = FlaskApp(ace, llm.create_image)

    discord_bot_token = get_environment_variable('DISCORD_BOT_TOKEN')
    discord_bot = DiscordBot(discord_bot_token, "stacey", ace, llm.create_image)

    flask_thread = threading.Thread(target=flask_app.run, daemon=True)
    discord_thread = threading.Thread(target=discord_bot.run, daemon=True)

    flask_thread.start()
    discord_thread.start()

    ace.start()
    flask_thread.join()
    discord_thread.join()

