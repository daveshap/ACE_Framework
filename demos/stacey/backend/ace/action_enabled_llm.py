import asyncio
import re
from typing import Optional

from ace.ace_layer import remove_memory_max_distance
from actions.action import Action
from actions.get_all_memories import GetAllMemories
from actions.get_web_content import GetWebContent
from actions.remove_memory import RemoveClosestMemory
from actions.save_memory import SaveMemory
from actions.search_web import SearchWeb
from actions.send_message_to_user import SendMessageToUser
from actions.set_next_alarm import SetNextAlarm
from actions.update_whiteboard import UpdateWhiteboard
from channels.communication_channel import CommunicationChannel
from llm.gpt import GptMessage, GPT
from memory.weaviate_memory_manager import WeaviateMemoryManager
from util import parse_json


class ActionEnabledLLM:
    def __init__(self, llm: GPT, model: str, memory_manager: WeaviateMemoryManager,
                 l3_agent_layer, serpapi_key: str):
        self.llm = llm
        self.model = model
        self.memory_manager = memory_manager
        self.l3_agent_layer = l3_agent_layer
        self.serpapi_key = serpapi_key

    async def talk_to_llm_and_execute_actions(
            self, communication_channel: CommunicationChannel, llm_messages: [GptMessage]):
        llm_response: GptMessage = await self.llm.create_conversation_completion(self.model, llm_messages)
        llm_response_content = llm_response["content"].strip()
        if llm_response_content:
            llm_messages.append(llm_response)

            print("Raw LLM response:\n" + llm_response_content)

            actions = self.parse_actions(communication_channel, llm_response_content)

            # Start all actions in parallel
            running_actions = []
            for action in actions:
                running_actions.append(
                    self.execute_action_and_send_result_to_llm(
                        action, communication_channel, llm_messages
                    )
                )
            # Wait for all actions to finish
            await asyncio.gather(*running_actions)
        else:
            print("LLM response was empty, so I guess we are done here.")

    async def execute_action_and_send_result_to_llm(
            self, action: Action, communication_channel: CommunicationChannel,
            llm_messages: [GptMessage]):
        print("Executing action: " + str(action))
        action_output: Optional[str] = await action.execute()
        if action_output is None:
            print("No response from action")
            return

        print(f"Got action output:\n{action_output}")

        print("I will add this to the llm conversation and talk to llm again.")

        llm_messages.append({
            "role": "user",
            "name": "action-output",
            "content": action_output
        })

        await self.talk_to_llm_and_execute_actions(communication_channel, llm_messages)

    def parse_actions(self, communication_channel: CommunicationChannel, text: str):
        # Extract JSON content from the text using regex
        json_match = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
        if not json_match:
            return []
        actions_string = json_match.group(1)

        action_data_list = parse_json(actions_string)

        if action_data_list is None or not isinstance(action_data_list, list):
            return []

        actions = []
        for action_data in action_data_list:
            action = self.parse_action(communication_channel, action_data)
            if action is not None:
                print("Adding action: " + str(action))
                actions.append(action)
            else:
                print("Unknown action: " + str(action_data))
                if communication_channel:
                    actions.append(SendMessageToUser(
                        communication_channel,
                        f"OK this is embarrassing. "
                        f"My brain asked me to do something that I don't know how to do: {action_data}"
                    ))

        return actions

    def parse_action(self, communication_channel: CommunicationChannel, action_data: dict):
        action_name = action_data.get("action")
        if action_name == "get_web_content":
            return GetWebContent(action_data["url"])
        elif action_name == "search_web":
            return SearchWeb(self.serpapi_key, action_data["query"])
        elif action_name == "send_message_to_user":
            return SendMessageToUser(communication_channel, action_data["text"])
        elif action_name == "update_whiteboard":
            return UpdateWhiteboard(self.l3_agent_layer, action_data["contents"])
        elif action_name == "set_next_alarm":
            return SetNextAlarm(self.l3_agent_layer, action_data["time_utc"])
        elif action_name == "save_memory":
            return SaveMemory(self.memory_manager, action_data["memory_string"])
        elif action_name == "get_all_memories":
            return GetAllMemories(self.memory_manager)
        elif action_name == "remove_closest_memory":
            return RemoveClosestMemory(self.memory_manager, action_data["memory_string"], remove_memory_max_distance)
        else:
            print(f"Warning: Unknown action: {action_name}")
            return None
