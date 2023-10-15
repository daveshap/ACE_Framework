from base.prompts import get_action_prompt, get_reasoning_input
from base.settings import Settings
import openai
from database.dao_models import LlmMessage, LayerConfigModel, Prompts, OpenAiGPTChatParameters
from typing import List
import re

import time
from datetime import datetime, timezone
import time

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reason(
    ancestral_prompt: str,
    input: str,
    source_bus: str,
    prompts: Prompts,
    llm_model_parameters: OpenAiGPTChatParameters,
    llm_messages: List[LlmMessage],
):
    start_time = time.time()
    start_time_fmt = datetime.fromtimestamp(start_time, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
    logger.info(f"Starting function reason() at {start_time_fmt}")

    reasoning_input = get_reasoning_input(
        input=input,
        source_bus=source_bus,
    )
    logger.info(f"{reasoning_input=}")
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

    end_time = time.time()
    end_time_fmt =  datetime.fromtimestamp(end_time, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
    elapsed_time = end_time - start_time
    logger.info(f"Function reason() ended at {end_time_fmt} and took {elapsed_time:.2f} seconds")

    return results

async def determine_action(
    ancestral_prompt: str,
    source_bus: str,
    reasoning_completion: LlmMessage,
    prompts: Prompts,
    llm_model_parameters: OpenAiGPTChatParameters,
    role_name: str,
    llm_messages: List[LlmMessage],
):
    start_time = time.time()
    start_time_fmt = datetime.fromtimestamp(start_time, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
    logger.info(f"Starting function determine_action() at {start_time_fmt}")

    data_bus_prompt = get_action_prompt(
        role_name=role_name,
        source_bus=source_bus,
        destination_bus="Data Bus",
        reasoning_completion=reasoning_completion,
        bus_rules=prompts.data_bus,
    )
    logger.info(f"{data_bus_prompt=}")

    control_bus_prompt = get_action_prompt(
        role_name=role_name,
        source_bus=source_bus,
        destination_bus="Control Bus",
        reasoning_completion=reasoning_completion,
        bus_rules=prompts.control_bus,
    )
    logger.info(f"{control_bus_prompt=}")

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
    logger.info(f"request data bus completion from chatgpt {datetime.fromtimestamp(time.time(), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    data_bus_action_completion = await get_completion(
        messages=data_bus_action,
        params=llm_model_parameters,
    )
    # data_bus_action_completion = (
    #     openai.ChatCompletion.create(
    #         messages=data_bus_action,
    #         **llm_model_parameters.model_dump(),
    #     ).choices[0].message
    # )
    logger.info(f"request contorl bus completion from chatgpt {datetime.fromtimestamp(time.time(), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    control_bus_action_completion = await get_completion(
        messages=control_bus_action,
        params=llm_model_parameters,
    )
    # control_bus_action_completion = (
    #     openai.ChatCompletion.create(
    #         messages=control_bus_action,
    #         **llm_model_parameters.model_dump(),
    #     ).choices[0].message
    # )

    end_time = time.time()
    end_time_fmt =  datetime.fromtimestamp(end_time, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S %Z')
    elapsed_time = end_time - start_time
    logger.info(f"Function determine_action() ended at {end_time_fmt} and took {elapsed_time:.2f} seconds")


    return data_bus_action_completion, control_bus_action_completion


async def get_completion(messages, params):

    return openai.ChatCompletion.create(
        messages=messages,
        **params.model_dump(),
    ).choices[0].message


def determine_none(input_text):
    match = re.search(r"\[Message\]\n(none)", input_text)

    if match:
        return "none"

    return input_text