# llm/gpt.py
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import List, TypedDict, Optional

import openai


class GptMessage(TypedDict):
    role: str
    name: Optional[str]
    content: str


class GPT:
    def __init__(self, api_key):
        self.api_key = api_key
        self.executor = ThreadPoolExecutor()

    async def create_chat_completion(self, model, system_message, user_message) -> str:
        response = await self.create_conversation_completion(model, [
            {"role": "system", "name": "system", "content": system_message},
            {"role": "user", "name": "user", "content": user_message}
        ])
        return response["content"]

    async def create_conversation_completion(self, model, conversation: List[GptMessage]) -> GptMessage:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._create_conversation_completion,
            model, conversation
        )

    def _create_conversation_completion(self, model, conversation: List[GptMessage]) -> GptMessage:
        """
        thread-blocking version of create_conversation_completion
        """
        print("_create_conversation_completion called for conversation: " + str(conversation))
        openai.api_key = self.api_key
        chat_completion = openai.ChatCompletion.create(
            model=model,
            messages=conversation
        )
        response = chat_completion.choices[0].message
        return response

    async def create_image(self, prompt, size='256x256') -> str:
        """
        :return: a short-lived image URL
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._create_image,
            prompt, size
        )

    def _create_image(self, prompt, size='256x256') -> str:
        """
        thread-blocking version of create_image
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

