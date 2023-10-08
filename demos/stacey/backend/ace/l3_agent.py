import asyncio
from datetime import datetime, timezone
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import ace.l3_agent_prompts as prompts
from ace.ace_layer import AceLayer
from ace.bus import Bus
from ace.layer_status import LayerStatus
from ace.types import ChatMessage, Memory
from actions.action import Action
from actions.cancel_all_scheduled_actions import CancelAllScheduledActions
from actions.cancel_scheduled_action import CancelScheduledAction
from actions.get_web_content import GetWebContent
from actions.list_scheduled_actions import GetScheduledActions
from actions.respond_to_user import RespondToUser
from actions.save_memory import SaveMemory
from actions.schedule_action import ScheduleAction
from channels.communication_channel import CommunicationChannel
from llm.gpt import GPT, GptMessage
from memory.weaviate_memory_manager import WeaviateMemoryManager
from util import parse_json

chat_history_length_short = 3

chat_history_length = 10

max_memories_to_include = 5


class L3AgentLayer(AceLayer):
    def __init__(self, llm: GPT, model,
                 southbound_bus: Bus, northbound_bus: Bus, memory_manager: WeaviateMemoryManager):
        super().__init__(3)
        self.llm = llm
        self.model = model
        self.southbound_bus = southbound_bus
        self.northbound_bus = northbound_bus
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.memory_manager = memory_manager

    async def process_incoming_user_message(self, communication_channel: CommunicationChannel):
        # Early out if I don't need to act, for example if I overheard a message that wasn't directed at me
        if not await self.should_act(communication_channel):
            return

        chat_history: [ChatMessage] = await communication_channel.get_message_history(chat_history_length)

        memories: [Memory] = []
        if len(chat_history) > 0:
            last_chat_message = chat_history[-1]
            memories: [Memory] = self.memory_manager.find_relevant_memories(
                self.stringify_chat_message(last_chat_message),
                max_memories_to_include
            )

        print("Found memories: " + str(memories))
        system_message = self.create_system_message()

        memories_if_any = ""
        if memories:
            memories_string = "\n".join(f"- <{memory['time_utc']}>: {memory['content']}" for memory in memories)
            memories_if_any = prompts.memories.replace("[memories]", memories_string)

        user_message = (
            prompts.act_on_user_input
            .replace("[communication_channel]", communication_channel.describe())
            .replace("[memories_if_any]", memories_if_any)
            .replace("[chat_history]", self.stringify_chat_history(chat_history))
        )
        llm_messages: [GptMessage] = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        print("System prompt: " + system_message)
        print("User prompt: " + user_message)
        await self.talk_to_llm_and_execute_actions(communication_channel, llm_messages)

    async def talk_to_llm_and_execute_actions(self, communication_channel, llm_messages: [GptMessage]):
        await self.set_status(LayerStatus.INFERRING)
        try:
            llm_response: GptMessage = await self.llm.create_conversation_completion(self.model, llm_messages)
            llm_response_content = llm_response["content"].strip()
            if llm_response_content:
                llm_messages.append(llm_response)

                print("Raw LLM response:\n" + llm_response_content)

                actions = self.parse_actions(communication_channel, llm_response_content)
                if len(actions) == 0:
                    # The LLM didn't return any actions, but it did return a text response. So respond with that.
                    actions.append(RespondToUser(communication_channel, llm_response_content))

                # Start all actions in parallell
                running_actions = []
                for action in actions:
                    running_actions.append(
                        self.execute_action_and_send_result_to_llm(action, communication_channel, llm_messages)
                    )
                # Wait for all actions to finish
                await asyncio.gather(*running_actions)
            else:
                print("LLM response was empty, so I guess we are done here.")
        finally:
            await self.set_status(LayerStatus.IDLE)

    async def execute_action_and_send_result_to_llm(
            self, action: Action, communication_channel: CommunicationChannel, llm_messages: [GptMessage]):
        print("Executing action: " + str(action))
        action_output: Optional[str] = await action.execute()
        if action_output is None:
            print("No response from action")
            return

        print("Got action output, will add to the llm messages and talk to llm again.")
        llm_messages.append({
            "role": "user",
            "name": "action-output",
            "content": action_output
        })

        await self.talk_to_llm_and_execute_actions(communication_channel, llm_messages)

    def parse_actions(self, communication_channel: CommunicationChannel, actions_string: str):
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
                print("Adding action to report unknown action")
                actions.append(RespondToUser(
                    communication_channel,
                    f"OK this is embarrassing. "
                    f"My brain asked me to do something that I don't know how to do: {action_data}"
                ))

        return actions

    def parse_action(self, communication_channel: CommunicationChannel, action_data: dict):
        action_name = action_data.get("action")
        if action_name == "get_web_content":
            return GetWebContent(action_data["url"])
        elif action_name == "respond_to_user":
            return RespondToUser(communication_channel, action_data["text"])
        elif action_name == "schedule_action":
            return self.create_schedule_action(communication_channel, action_data)
        elif action_name == "get_scheduled_actions":
            return GetScheduledActions(self.scheduler)
        elif action_name == "cancel_all_scheduled_actions":
            return CancelAllScheduledActions(self.scheduler)
        elif action_name == "cancel_scheduled_action":
            return CancelScheduledAction(self.scheduler, action_data["job_id"])
        elif action_name == "save_memory":
            return SaveMemory(self.memory_manager, action_data["memory_string"])
        else:
            print(f"Warning: Unknown action: {action_name}")
            return None

    def create_schedule_action(self, communication_channel: CommunicationChannel, action_data: dict):
        print("Scheduling action: " + str(action_data))
        action_data_to_schedule = action_data.get("action_to_schedule", {})
        delay_seconds = action_data.get("delay_seconds", 0)
        if not action_data_to_schedule or delay_seconds <= 0:
            print(f"Warning: Invalid schedule_action data: {action_data}")
            return None

        action_to_schedule = self.parse_action(communication_channel, action_data_to_schedule)
        if action_to_schedule is None:
            print(f"Warning: Invalid schedule_action data: {action_data}")
            return None

        return ScheduleAction(self.scheduler, communication_channel, action_to_schedule, delay_seconds)

    def create_system_message(self):
        current_time_utc = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        system_message = f"""
                {prompts.self_identity}
                {prompts.personality}
                {prompts.knowledge.replace("[current_time_utc]", current_time_utc)}
                {prompts.media_replacement}
                {prompts.actions}
            """
        return system_message

    async def should_act(self, communication_channel: CommunicationChannel):
        """
        Ask the LLM whether this is a message that we should act upon.
        This is a cheaper request than asking the LLM to generate a response,
        allows us to early-out for unrelated messages.
        """

        message_history: [ChatMessage] = await communication_channel.get_message_history(
            chat_history_length_short
        )

        prompt = prompts.decide_whether_to_respond_prompt.format(
            messages=self.stringify_chat_history(message_history)
        )

        print(f"Prompt to determine if we should respond:\n {prompt}")
        await self.set_status(LayerStatus.INFERRING)
        try:
            response = await self.llm.create_conversation_completion(
                self.model,
                [{"role": "user", "name": "user", "content": prompt}]
            )
            response_content = response['content'].strip().lower()

            print(f"Response to prompt: {response_content}")

            return response_content.startswith("yes")
        finally:
            await self.set_status(LayerStatus.IDLE)

    def stringify_chat_history(self, conversation: [ChatMessage]):
        return "\n".join(f"- {self.stringify_chat_message(message)}" for message in conversation)

    def stringify_chat_message(self, chat_message: ChatMessage):
        return f"<{chat_message['time_utc']}> [{chat_message['sender']}] {chat_message['content']}"

