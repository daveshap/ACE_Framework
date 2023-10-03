import openai
from typing import List, Dict

def generate_completion(
    identity: str, 
    new_message: str, 
    memory: List[Dict[str, str]],
    temperature: int,
    model: str,
    openai_api_key: str,
):
    openai.api_key = openai_api_key
    primary_directive = {"role": "system", "content": identity}
    new_prompt = {"role": "user", "content": new_message}
    conversation = (
        [primary_directive] +
        memory +
        [new_prompt]
    )
    completion = openai.ChatCompletion.create(
        model=model,
        messages=conversation,
        temperature=temperature,
    )
    response = completion.choices[0].message

    response_memory = memory.copy()
    response_memory.append(new_prompt)
    response_memory.append(response)

    return response, response_memory
