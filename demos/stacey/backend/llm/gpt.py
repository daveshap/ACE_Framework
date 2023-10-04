# llm/gpt.py
from typing import List, TypedDict

import litellm
import openai


class GptMessage(TypedDict):
    role: str
    content: str


class GPT:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_chat_completion(self, model, system_message, user_message) -> str:
        return self.create_conversation_completion(model, [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ])["content"]

    def create_conversation_completion(self, model, conversation: List[GptMessage]) -> GptMessage:
        litellm.api_key = self.api_key
        chat_completion = litellm.completion(
            model=model,
            messages=conversation
        )
        response = chat_completion.choices[0].message
        return response

    def create_image(self, prompt, size='256x256') -> str:
        """
        :return: a short-lived image URL
        """
        print("Generating image for prompt: " + prompt)
        openai.api_key = self.api_key
        result = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size
        )
        image_url = result.data[0].url
        print(".... finished generating image for prompt" + prompt + ":\n" + image_url)
        return image_url

