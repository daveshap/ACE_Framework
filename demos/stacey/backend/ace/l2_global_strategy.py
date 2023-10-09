# l2_global_strategy.py
from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import ace.l2_global_strategy_prompts as prompts
from channels.communication_channel import CommunicationChannel
from llm.gpt import GptMessage, GPT
from .ace_layer import AceLayer
from .action_enabled_llm import ActionEnabledLLM
from .l1_aspirational import L1AspirationalLayer
from .types import stringify_chat_history

client_agents = []

chat_history_length = 10


class L2GlobalStrategyLayer(AceLayer):
    def __init__(self, llm: GPT, model, memory_manager, l1_aspirational_layer: L1AspirationalLayer):
        super().__init__("2")
        self.llm = llm
        self.model = model
        self.l1_aspirational_layer = l1_aspirational_layer
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.action_enabled_llm = ActionEnabledLLM(llm, model, self.scheduler, memory_manager, self)

    async def enroll_client(self, user_name, communication_channel: CommunicationChannel):
        client_agent = ClientAgent(self.action_enabled_llm, user_name, self.l1_aspirational_layer)
        client_agents.append(client_agent)
        await client_agent.act(communication_channel)

    async def find_client_agent(self, user_name):
        for client in client_agents:
            if client.client_name == user_name:
                return client
        return None


class ClientAgent:
    """
    An agent working on the behalf of one specific client.
    """

    def __init__(
            self, action_enabled_llm: ActionEnabledLLM, client_name: str, l1_aspirational_layer):
        self.action_enabled_llm = action_enabled_llm
        self.client_name = client_name
        self.l1_aspirational_layer = l1_aspirational_layer
        self.whiteboard = ""

    async def update_whiteboard(self, contents):
        self.whiteboard = contents

    async def act(self, communication_channel: Optional[CommunicationChannel]):
        print("Strategy Agent for " + self.client_name + " is going to act")
        system_message = self.l1_aspirational_layer.get_consitution()

        user_name = None
        chat_history_if_available = ""
        if communication_channel:
            chat_history = await communication_channel.get_message_history(chat_history_length)
            if chat_history:
                user_name = chat_history[-1]['sender']
                chat_history_if_available = (
                    prompts.chat_history
                    .replace("[client_name]", self.client_name)
                    .replace("[communication_channel]", communication_channel.describe())
                    .replace("[chat_history]", stringify_chat_history(chat_history))
                )

        user_message = (
            prompts.act
            .replace("[user_name]", self.client_name)
            .replace("[chat_history_if_available]", chat_history_if_available)
            .replace("[communication_channel]", communication_channel.describe())
            .replace("[whiteboard]", self.whiteboard)
        )
        llm_messages: [GptMessage] = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        print("System prompt: " + system_message)
        print("User prompt: " + user_message)
        await self.action_enabled_llm.talk_to_llm_and_execute_actions(communication_channel, user_name, llm_messages)
