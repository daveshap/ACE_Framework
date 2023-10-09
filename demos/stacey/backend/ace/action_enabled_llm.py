import asyncio
import json
import re
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ace.ace_layer import remove_memory_max_distance
from actions.action import Action
from actions.cancel_all_scheduled_actions import CancelAllScheduledActions
from actions.cancel_scheduled_action import CancelScheduledAction
from actions.enroll_client import EnrollClient
from actions.get_all_memories import GetAllMemories
from actions.get_web_content import GetWebContent
from actions.list_scheduled_actions import GetScheduledActions
from actions.remove_memory import RemoveClosestMemory
from actions.respond_to_user import RespondToUser
from actions.save_memory import SaveMemory
from actions.schedule_action import ScheduleAction
from actions.update_whiteboard import UpdateWhiteboard
from channels.communication_channel import CommunicationChannel
from llm.gpt import GptMessage, GPT
from memory.weaviate_memory_manager import WeaviateMemoryManager
from util import parse_json


class ActionEnabledLLM:
    def __init__(self, llm: GPT, model: str, scheduler: AsyncIOScheduler, memory_manager: WeaviateMemoryManager,
                 l2_global_strategy_layer):
        self.llm = llm
        self.model = model
        self.scheduler = scheduler
        self.memory_manager = memory_manager
        self.l2_global_strategy_layer = l2_global_strategy_layer

    async def talk_to_llm_and_execute_actions(
            self, communication_channel: CommunicationChannel, user_name: Optional[str], llm_messages: [GptMessage]):
        llm_response: GptMessage = await self.llm.create_conversation_completion(self.model, llm_messages)
        llm_response_content = llm_response["content"].strip()
        if llm_response_content:
            llm_messages.append(llm_response)

            print("Raw LLM response:\n" + llm_response_content)

            actions = self.parse_actions(communication_channel, user_name, llm_response_content)

            # Start all actions in parallel
            running_actions = []
            for action in actions:
                running_actions.append(
                    self.execute_action_and_send_result_to_llm(
                        action, communication_channel, user_name, llm_messages
                    )
                )
            # Wait for all actions to finish
            await asyncio.gather(*running_actions)
        else:
            print("LLM response was empty, so I guess we are done here.")

    async def execute_action_and_send_result_to_llm(
            self, action: Action, communication_channel: CommunicationChannel, user_name: Optional[str],
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

        await self.talk_to_llm_and_execute_actions(communication_channel, user_name, llm_messages)

    def parse_actions(self, communication_channel: CommunicationChannel, user_name, text: str):
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
            action = self.parse_action(communication_channel, user_name, action_data)
            if action is not None:
                print("Adding action: " + str(action))
                actions.append(action)
            else:
                print("Adding action to report unknown action")
                actions.append(RespondToUser(
                    communication_channel,
                    f"OK this is embarrassing. "
                    f"My brain asked me to do something that I don't know how to do: {action_data}"
                ))

        return actions

    def parse_action(self, communication_channel: CommunicationChannel, user_name: Optional[str], action_data: dict):
        action_name = action_data.get("action")
        if action_name == "get_web_content":
            return GetWebContent(action_data["url"])
        elif action_name == "respond_to_user" or action_name == "message_to_client":
            return RespondToUser(communication_channel, action_data["text"])
        elif action_name == "enroll_client":
            return EnrollClient(self.l2_global_strategy_layer, user_name, communication_channel)
        elif action_name == "update_whiteboard":
            content_string = json.dumps(action_data["contents"], indent=2)
            return UpdateWhiteboard(self.l2_global_strategy_layer, user_name, content_string)
        elif action_name == "schedule_action":
            return self.create_schedule_action(communication_channel, user_name, action_data)
        elif action_name == "get_scheduled_actions":
            return GetScheduledActions(self.scheduler)
        elif action_name == "cancel_all_scheduled_actions":
            return CancelAllScheduledActions(self.scheduler)
        elif action_name == "cancel_scheduled_action":
            return CancelScheduledAction(self.scheduler, action_data["job_id"])
        elif action_name == "save_memory":
            return SaveMemory(self.memory_manager, action_data["memory_string"])
        elif action_name == "get_all_memories":
            return GetAllMemories(self.memory_manager)
        elif action_name == "remove_closest_memory":
            return RemoveClosestMemory(self.memory_manager, action_data["memory_string"], remove_memory_max_distance)
        else:
            print(f"Warning: Unknown action: {action_name}")
            return None

    def create_schedule_action(self, communication_channel: CommunicationChannel, user_name: str, action_data: dict):
        print("Scheduling action: " + str(action_data))
        action_data_to_schedule = action_data.get("action_to_schedule", {})
        delay_seconds = action_data.get("delay_seconds", 0)
        if not action_data_to_schedule or delay_seconds <= 0:
            print(f"Warning: Invalid schedule_action data: {action_data}")
            return None

        action_to_schedule = self.parse_action(communication_channel, user_name, action_data_to_schedule)
        if action_to_schedule is None:
            print(f"Warning: Invalid schedule_action data: {action_data}")
            return None

        return ScheduleAction(self.scheduler, communication_channel, action_to_schedule, delay_seconds)
