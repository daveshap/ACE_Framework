import openai
from typing import List
from schema import Prompts, OpenAiGPTChatParameters

def generate_bus_message(
        layer_name: str,
        prompts: Prompts,
        source_bus: str,
        destination_bus: str,
        llm_messages: List,
        llm_model_name: str,
        llm_model_parameters: OpenAiGPTChatParameters,
        openai_api_key: str,
):
    openai.api_key = openai_api_key

    reasoning_prompt = (
f"""
# You Received a MESSAGE From the SOURCE BUS
## MESSAGE
{prompts.input}

## SOURCE BUS
{source_bus}
"""
    )

    reasoning_messages = [
        {"role": "system", "content": f"{prompts.identity}\n\n{prompts.reasoning}"},
    ] + llm_messages + [
        {"role": "user", "content": reasoning_prompt}
    ]

    reasoning_response = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=reasoning_messages,
        **llm_model_parameters.model_dump(exclude_none=True, exclude_unset=True),
    )
    reasoning_result = reasoning_response.choices[0].message

    action_prompt = (
f"""
# Given Your Role as the {layer_name} in the ACE framework
Consider the INPUT, YOUR REASONING about it, and BUS RULES to decide what, if any, message you should place on the {destination_bus}

## INPUT
Input source bus = {source_bus}
{prompts.input}
## YOUR REASONING
{reasoning_result}
## BUS RULES
{prompts.bus}
"""
    )

    bus_action = [
        {"role": "system", "content": f"{prompts.identity}\n{prompts.reasoning}"},
    ] + llm_messages + [
        {"role": "user", "content": action_prompt}]

    bus_action_response = openai.ChatCompletion.create(
        model=llm_model_name,
        messages=bus_action,
        **llm_model_parameters
    )

    bus_action_result = bus_action_response.choices[0].message

    return reasoning_result, bus_action_result, llm_messages
