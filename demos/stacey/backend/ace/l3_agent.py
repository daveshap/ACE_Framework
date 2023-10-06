import asyncio
from datetime import datetime
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ace.ace_layer import AceLayer
from ace.bus import Bus
import ace.l3_agent_prompts as prompts
from ace.layer_status import LayerStatus
from actions.action import Action
from actions.cancel_all_scheduled_actions import CancelAllScheduledActions
from actions.cancel_scheduled_action import CancelScheduledAction
from actions.get_web_content import GetWebContent
from actions.list_scheduled_actions import GetScheduledActions
from actions.respond_to_user import RespondToUser
from actions.schedule_action import ScheduleAction
from channels.communication_channel import CommunicationChannel
from llm.gpt import GPT, GptMessage
from util import parse_json

how_many_messages_to_include_when_determining_if_agent_should_respond = 3

how_many_messages_to_include_when_generating_response = 10


class L3AgentLayer(AceLayer):
    def __init__(self, llm: GPT, model,
                 southbound_bus: Bus, northbound_bus: Bus):
        super().__init__(3)
        self.llm = llm
        self.model = model
        self.southbound_bus = southbound_bus
        self.northbound_bus = northbound_bus
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

    async def process_incoming_user_message(self, communication_channel: CommunicationChannel):
        # Check if I need to act
        if not await self.should_act(communication_channel):
            # I don't need to respond or talk to the LLM. Maybe I overheard a message that wasn't directed at me
            return

        # Build up the conversation
        message_history: [GptMessage] = await communication_channel.get_message_history(
            how_many_messages_to_include_when_generating_response
        )
        system_message = self.create_system_message(communication_channel)
        conversation = [{"role": "system", "content": system_message}] + message_history

        # Talk to the LLM
        await self.talk_to_llm_and_execute_actions(communication_channel, conversation)

    async def talk_to_llm_and_execute_actions(self, communication_channel, conversation):
        await self.set_status(LayerStatus.INFERRING)
        try:
            llm_response: GptMessage = await self.llm.create_conversation_completion(self.model, conversation)
            llm_response_content = llm_response["content"].strip()
            if llm_response_content:
                conversation.append(llm_response)

                print("Raw LLM response:\n" + llm_response_content)

                actions = self.parse_actions(communication_channel, llm_response_content)
                if len(actions) == 0:
                    # The LLM didn't return any actions, but it did return a text response. So respond with that.
                    actions.append(RespondToUser(communication_channel, llm_response_content))

                # Start all actions in parallell
                running_actions = []
                for action in actions:
                    running_actions.append(
                        self.execute_action_and_send_result_to_llm(action, communication_channel, conversation)
                    )
                # Wait for all actions to finish
                await asyncio.gather(*running_actions)
            else:
                print("LLM response was empty, so I guess we are done here.")
        finally:
            await self.set_status(LayerStatus.IDLE)

    async def execute_action_and_send_result_to_llm(
            self, action: Action, communication_channel: CommunicationChannel, conversation: [GptMessage]):
        print("Executing action: " + str(action))
        action_output: Optional[str] = await action.execute()
        if action_output is None:
            print("No response from action")
            return

        print("Got action output, will add to the conversation and talk to llm again.")
        conversation.append({"role": "user", "name": "action-output", "content": action_output})

        await self.talk_to_llm_and_execute_actions(communication_channel, conversation)

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

    def create_system_message(self, communication_channel: CommunicationChannel):
        current_time = datetime.now().astimezone()
        formatted_time = f"{current_time.strftime('%A')} {current_time.isoformat()}"
        system_message = f"""
                {prompts.self_identity}
                {prompts.knowledge.replace("[current_time]", formatted_time)}
                {prompts.media_replacement}
                {prompts.actions}
                {prompts.communication_channel.replace(
            "[current_communication_channel]", communication_channel.describe()
                )}
                {prompts.personality}
                {prompts.behaviour}
            """
        return system_message

    async def should_act(self, communication_channel: CommunicationChannel):
        """
        Ask the LLM whether this is a message that we should act upon
        """

        conversation: [GptMessage] = await communication_channel.get_message_history(
            how_many_messages_to_include_when_determining_if_agent_should_respond
        )

        prompt = prompts.decide_whether_to_respond_prompt.format(
            messages="\n".join([f"- [{message['name']}] {message['content']}" for message in conversation])
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

