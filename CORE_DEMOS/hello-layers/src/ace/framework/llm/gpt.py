# llm/gpt.py
from typing import List, TypedDict, Optional

import openai


class GptMessage(TypedDict):
    role: str
    name: Optional[str]
    content: str


class GPT:

    def _create_conversation_completion(self, model, conversation: List[GptMessage]) -> GptMessage:
        # print("_create_conversation_completion called for conversation: " + str(conversation))
        # openai.api_key = self.api_key
        chat_completion = openai.ChatCompletion.create(
            model=model,
            messages=conversation
        )
        response = chat_completion.choices[0].message
        return response

    def _create_image(self, prompt, size='256x256') -> str:
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

