from dotenv import load_dotenv

from ace.ace_system import AceSystem
from channels.web.fastapi_app import FastApiApp
from llm.gpt import GPT
from util import get_environment_variable

load_dotenv()
openai_api_key = get_environment_variable('OPENAI_API_KEY')
llm = GPT(openai_api_key)
ace = AceSystem(llm, get_environment_variable("DEFAULT_MODEL"))
ace.start()
fastapi_app = FastApiApp(ace, llm.create_image)
fastapi_app.run()
