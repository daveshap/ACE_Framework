import openai
from typing import List, Dict

def generate_bus_message(
        input: str,
        identity: str,
        reasoning: str,
        bus_prompt: str,
        source_bus: str,
        destination_bus: str,
        llm_messages: List,
        llm_model_name: str,
        llm_model_parameters: str,
        openai_api_key: str,
):
    openai.api_key = openai_api_key

    reasoning_messages = llm_messages + [
        {"role": "system", "content": identity},
        {"role": "system", "content": reasoning},
        {"role": "user", "content": f"You recieved a message from the {source_bus}"},
        {"role": "user", "content": input},
    ]
    reasoning_response = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=reasoning_messages,
        **llm_model_parameters
    )
    reasoning_result = reasoning_response.choices[0].message

    bus_action = llm_messages + [
        {"role": "system", "content": identity},
        {"role": "system", "content": reasoning},
        {"role": "user", "content": reasoning_result},
        {"role": "user", "content": f"You recieved a message from the {source_bus}"},
        {"role": "user", "content": input},
        {"role": "user", "content": f"Decide if you should place a message on the {destination_bus}"},
        {"role": "user", "content": bus_prompt},
    ]
    bus_action_response = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=bus_action,
        **llm_model_parameters
    )

    bus_action_result = bus_action_response.choices[0].message

    return reasoning_result, bus_action_result
