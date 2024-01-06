# llm/gpt.py
from typing import List, TypedDict, Optional

from openai import OpenAI

from ace.logger import Logger


class GptMessage(TypedDict):
    role: str
    name: Optional[str]
    content: str


class GPT:
    def __init__(self):
        self.log = Logger(self.__class__.__name__)
        self.client = OpenAI()

    def create_conversation_completion(
        self, model, conversation: List[GptMessage]
    ) -> GptMessage:
        # print("_create_conversation_completion called for conversation: " + str(conversation))
        # openai.api_key = self.api_key
        chat_completion = self.client.chat.completions.create(
            model=model, messages=conversation
        )
        response = chat_completion.choices[0].message
        return response

    def create_image(self, prompt, size="256x256") -> str:
        self.log.debug("Generating image for prompt: " + prompt)
        openai.api_key = self.api_key
        result = openai.Image.create(prompt=prompt, n=1, size=size)
        image_url = result.data[0].url
        self.log.debug(
            ".... finished generating image for prompt" + prompt + ":\n" + image_url
        )
        return image_url
