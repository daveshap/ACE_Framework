from ace.ace_system import AceSystem
from channels.discord.discord_bot import DiscordBot
from llm.gpt import GPT
from util import get_environment_variable

openai_api_key = get_environment_variable('OPENAI_API_KEY')
llm = GPT(openai_api_key)
discord_bot_token = get_environment_variable('DISCORD_BOT_TOKEN')
ace = AceSystem(llm, get_environment_variable("DEFAULT_MODEL"))
discord_bot = DiscordBot(discord_bot_token, "stacey", ace, llm.create_image)
discord_bot.run()
