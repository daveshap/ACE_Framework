# gpt.py
import os
import pprint

import openai
from dotenv import load_dotenv
load_dotenv()


def create_chat_completion(model, conversation):
    print(f"  Sending conversation to {model}: {pprint.pformat(conversation)}")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    chat_completion = openai.ChatCompletion.create(
        model=model,
        messages=conversation
    )
    return chat_completion.choices[0].message


def create_image(prompt, size='256x256'):
    """
    Returns a short-lived image URL
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    result = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size
    )
    return result.data[0].url


if __name__ == '__main__':
    print(create_image('A painting of a cat sitting on a chair'))