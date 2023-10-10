from base.prompts import get_action_prompt, get_reasoning_input
from base.settings import Settings
import openai
from database.dao_models import LlmMessage, LayerConfigModel, Prompts, OpenAiGPTChatParameters
from typing import List
import re


def reason(
    ancestral_prompt: str,
    input: str,
    source_bus: str,
    prompts: Prompts,
    llm_model_parameters: OpenAiGPTChatParameters,
    llm_messages: List[LlmMessage],
):
    reasoning_input = get_reasoning_input(
        input=input,
        source_bus=source_bus,
    )
    system_message = "\n\n".join(
        [
            prompts.identity,
            ancestral_prompt,
            prompts.reasoning,
        ]
    )

    reasoning_messages = (
        [{"role": "system", "content": system_message}]
        + llm_messages
        + [{"role": "user", "content": reasoning_input}]
    )

    reasoning_response = openai.ChatCompletion.create(
        messages=reasoning_messages,
        **llm_model_parameters.model_dump(
            exclude_none=True,
            exclude_unset=True,
        ),
    )
    results = reasoning_response.choices[0].message
    return results

def determine_action(
    ancestral_prompt: str,
    source_bus: str,
    reasoning_completion: LlmMessage,
    prompts: Prompts,
    llm_model_parameters: OpenAiGPTChatParameters,
    role_name: str,
    llm_messages: List[LlmMessage],
):
    data_bus_prompt = get_action_prompt(
        role_name=role_name,
        source_bus=source_bus,
        destination_bus="Data Bus",
        reasoning_completion=reasoning_completion,
        bus_rules=prompts.data_bus,
    )
    control_bus_prompt = get_action_prompt(
        role_name=role_name,
        source_bus=source_bus,
        destination_bus="Control Bus",
        reasoning_completion=reasoning_completion,
        bus_rules=prompts.control_bus,
    )
    system_message = "\n\n".join(
        [
            prompts.identity,
            ancestral_prompt,
            # prompts.reasoning, # This is likely going to confuse the LLM layer because the first reasoning completion would be better.
        ]
    )
    data_bus_action = (
        [{"role": "system","content": system_message}]
        + llm_messages
        + [{"role": "user", "content": data_bus_prompt}]
    )
    control_bus_action = (
        [{"role": "system","content": system_message}]
        + llm_messages
        + [{"role": "user", "content": control_bus_prompt}]
    )
    data_bus_action_completion = (
        openai.ChatCompletion.create(
            messages=data_bus_action,
            **llm_model_parameters.model_dump(),
        ).choices[0].message
    )
    control_bus_action_completion = (
        openai.ChatCompletion.create(
            messages=control_bus_action,
            **llm_model_parameters.model_dump(),
        ).choices[0].message
    )
    return data_bus_action_completion, control_bus_action_completion


def determine_none(input_text):
    match = re.search(r"\[Message\]\n(none)", input_text)

    if match:
        return "none"

    return input_text