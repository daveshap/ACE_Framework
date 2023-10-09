from apscheduler.schedulers.asyncio import AsyncIOScheduler

import ace.receptionist_prompts as prompts
from ace.ace_layer import AceLayer
from ace.action_enabled_llm import ActionEnabledLLM
from ace.l1_aspirational import L1AspirationalLayer
from ace.l2_global_strategy import L2GlobalStrategyLayer, ClientAgent
from ace.layer_status import LayerStatus
from ace.types import ChatMessage, stringify_chat_history
from channels.communication_channel import CommunicationChannel
from llm.gpt import GPT, GptMessage
from memory.weaviate_memory_manager import WeaviateMemoryManager

chat_history_length_short = 3
chat_history_length = 10


class Receptionist(AceLayer):
    def __init__(self,  llm: GPT, model: str,
                 memory_manager: WeaviateMemoryManager,
                 l1_aspirational_layer: L1AspirationalLayer,
                 l2_global_strategy_layer: L2GlobalStrategyLayer):
        super().__init__("Receptionist")
        self.llm = llm
        self.model = model
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.action_enabled_llm = ActionEnabledLLM(llm, model, self.scheduler, memory_manager, l2_global_strategy_layer)
        self.l1_aspirational_layer = l1_aspirational_layer
        self.l2_global_strategy_layer = l2_global_strategy_layer

    async def process_incoming_user_message(self, communication_channel: CommunicationChannel):
        # Early out if I don't need to act, for example if I overheard a message that wasn't directed at me
        if not await self.should_act(communication_channel):
            return

        chat_history: [ChatMessage] = await communication_channel.get_message_history(chat_history_length)
        if not chat_history:
            print("Warning: process_incoming_user_message was called with no chat history. That's weird. Ignoring.")
            return
        last_chat_message = chat_history[-1]
        user_name = last_chat_message['sender']

        client_agent: ClientAgent = await self.l2_global_strategy_layer.find_client_agent(user_name)
        if client_agent:
            await client_agent.act(communication_channel)
        else:
            await self.respond_as_receptionist(chat_history, communication_channel, user_name)

    async def respond_as_receptionist(self, chat_history: [ChatMessage], communication_channel, user_name):
        system_message = self.l1_aspirational_layer.get_consitution()
        user_message = (
            prompts.act_on_user_input
            .replace("[user_name]", user_name)
            .replace("[communication_channel]", communication_channel.describe())
            .replace("[chat_history]", stringify_chat_history(chat_history))
        )
        llm_messages: [GptMessage] = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        print("System prompt: " + system_message)
        print("User prompt: " + user_message)
        await self.action_enabled_llm.talk_to_llm_and_execute_actions(communication_channel, user_name, llm_messages)

    async def should_act(self, communication_channel: CommunicationChannel):
        """
        Ask the LLM whether this is a message that we should act upon.
        This is a cheaper request than asking the LLM to generate a response,
        allows us to early-out for unrelated messages.
        """

        message_history: [ChatMessage] = await communication_channel.get_message_history(
            chat_history_length_short
        )

        prompt = prompts.decide_whether_to_respond.format(
            messages=stringify_chat_history(message_history)
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
