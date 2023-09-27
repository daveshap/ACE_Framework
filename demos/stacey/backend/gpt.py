import os
import openai

def create_chat_completion(model, conversation):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    chat_completion = openai.ChatCompletion.create(
        model=model,
        messages=conversation
    )
    return chat_completion.choices[0].message
