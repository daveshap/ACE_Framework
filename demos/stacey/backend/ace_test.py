import os

from dotenv import load_dotenv

import config
from ace.ace_system import AceSystem
from llm.gpt import GPT

load_dotenv()

if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set.")

    llm = GPT(api_key)
    ace_system = AceSystem(llm, config.default_model)
    ace_system.start()

    while True:
        user_input = input("Type a message to send to the north bus: ")
        if user_input.lower() == 'exit':
            print("Exiting AceTest...")
            break
        ace_system.northbound_bus.publish(10, user_input)
