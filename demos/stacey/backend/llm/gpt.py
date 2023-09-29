# llm/gpt.py
import openai


class GPT:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_chat_completion(self, model, system_message, user_message):
        """
        :return: response string
        """
        return self.create_conversation_completion(model, [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]).content

    def create_conversation_completion(self, model, conversation):
        """
        :param conversation: an array of role/content pairs
        :return: a single role/content pair
        """
        openai.api_key = self.api_key
        chat_completion = openai.ChatCompletion.create(
            model=model,
            messages=conversation
        )
        response = chat_completion.choices[0].message
        return response

    def create_image(self, prompt, size='256x256'):
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

