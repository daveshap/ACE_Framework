# gpt.py
import os

import openai
from dotenv import load_dotenv

load_dotenv()


def create_chat_completion(model, conversation):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    chat_completion = openai.ChatCompletion.create(
        model=model,
        messages=conversation
    )
    response = chat_completion.choices[0].message
    return response


def create_image(prompt, size='256x256'):
    """
    Returns a short-lived image URL
    """
    print("Generating image for prompt: " + prompt)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    result = openai.Image.create(
        prompt=prompt,
        n=1,
        size=size
    )
    image_url = result.data[0].url
    print(".... finished generating image for prompt" + prompt + ":\n" + image_url)
    return image_url


if __name__ == '__main__':
    print(create_image('A painting of a cat sitting on a chair'))