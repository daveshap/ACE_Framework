from ace.ace_system import AceSystem
from channels.discord.discord_bot import DiscordBot
from llm.gpt import GPT
from media.giphy_finder import GiphyFinder
from util import get_environment_variable

openai_api_key = get_environment_variable('OPENAI_API_KEY')
llm = GPT(openai_api_key)
discord_bot_token = get_environment_variable('DISCORD_BOT_TOKEN')
ace = AceSystem(llm, get_environment_variable("DEFAULT_MODEL"))
giphy = GiphyFinder(get_environment_variable('GIPHY_API_KEY'))
media_generators = [
    {"keyword": "IMAGE", "generator_function": llm.create_image},
    {"keyword": "GIF", "generator_function": giphy.get_giphy_url}
]

discord_bot = DiscordBot(discord_bot_token, "stacey", ace, media_generators)
discord_bot.run()
