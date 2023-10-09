import openai
from typing import List
from schema import Prompts, OpenAiGPTChatParameters, LlmMessage
import re

def generate_bus_message(
        ancestral_prompt: str,
        input: str,
        layer_name: str,
        prompts: Prompts,
        source_bus: str,
        llm_messages: List[LlmMessage],
        llm_model_parameters: OpenAiGPTChatParameters,
        openai_api_key: str,
):
    openai.api_key = openai_api_key

    reasoning_result = get_reasoning(
        ancestral_prompt=ancestral_prompt,
        input=input,
        prompts=prompts,
        source_bus=source_bus,
        llm_messages=llm_messages,
        llm_model_parameters=llm_model_parameters,
    )

    data_bus_action_result = get_bus_action(
        ancestral_prompt=ancestral_prompt,
        input=input,
        layer_name=layer_name,
        prompts=prompts,
        source_bus=source_bus,
        destination_bus="Data Bus",
        bus_prompt=prompts.data_bus,
        llm_messages=llm_messages,
        llm_model_parameters=llm_model_parameters,
        reasoning_result=reasoning_result
    )

    control_bus_action_result = get_bus_action(
        ancestral_prompt=ancestral_prompt,
        input=input,
        layer_name=layer_name,
        prompts=prompts,
        source_bus=source_bus,
        destination_bus="Control Bus",
        bus_prompt=prompts.control_bus,
        llm_messages=llm_messages,
        llm_model_parameters=llm_model_parameters,
        reasoning_result=reasoning_result
    )

    return reasoning_result, data_bus_action_result, control_bus_action_result

def get_reasoning(
    ancestral_prompt: str,
    input: str, 
    prompts: Prompts,
    source_bus: str,
    llm_messages: str,
    llm_model_parameters: OpenAiGPTChatParameters,
):
    reasoning_prompt = (
f"""
# You Received a MESSAGE From the SOURCE BUS
## MESSAGE
{input}

## SOURCE BUS
{source_bus}
"""
    )
    system_prompt = f"{prompts.identity}\n\n{ancestral_prompt}\n\n{prompts.reasoning}"
    reasoning_messages = [
        {"role": "system", "content": system_prompt},
    ] + llm_messages + [
        {"role": "user", "content": reasoning_prompt}
    ]

    reasoning_response = openai.ChatCompletion.create(
        messages=reasoning_messages,
        **llm_model_parameters.model_dump(exclude_none=True, exclude_unset=True),
    )
    reasoning_result = reasoning_response.choices[0].message
    return reasoning_result

def get_bus_action(
    ancestral_prompt: str,
    input: str,
    layer_name: str, 
    source_bus: str,
    destination_bus: str,
    bus_prompt: str,
    prompts: Prompts,
    llm_messages: List[LlmMessage],
    llm_model_parameters: OpenAiGPTChatParameters,
    reasoning_result: str,
):
    data_bus_action_prompt = (
f"""
# Given Your Role as the {layer_name} in the ACE framework
Consider the INPUT, YOUR REASONING about it, and BUS RULES to decide what, if any, message you should place on the {destination_bus}

## INPUT
Input source bus = {source_bus}
{input}

## YOUR REASONING
{reasoning_result}

## BUS RULES
{bus_prompt}
"""
    )
    system_prompt = f"{ancestral_prompt}\n\n{prompts.identity}\n\n{prompts.reasoning}"
    data_bus_action = [
        {"role": "system", "content": system_prompt},
    ] + llm_messages + [
        {"role": "user", "content": data_bus_action_prompt}]

    bus_action_response = openai.ChatCompletion.create(
        messages=data_bus_action,
        **llm_model_parameters.model_dump(exclude_none=True, exclude_unset=True),
    )

    data_bus_action_result = bus_action_response.choices[0].message
    return data_bus_action_result


def determine_none(self, input_text):
    match = re.search(r"\[Message\]\n(none)", input_text)

    if match:
        return "none"

    return input_text