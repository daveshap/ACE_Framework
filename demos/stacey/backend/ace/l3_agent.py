import asyncio
from datetime import datetime
from typing import Optional

from ace.ace_layer import AceLayer
from ace.bus import Bus
from ace.layer_status import LayerStatus
from actions.action import Action
from actions.get_web_content import GetWebContent
from actions.respond_to_user import RespondToUser
from actions.schedule_action import ScheduleAction
from channels.communication_channel import CommunicationChannel
from llm.gpt import GPT, GptMessage
from util import parse_json

self_identity = """
# Self identity:
You are Stacey, a proof-of-concept implementation of the ACE Framework.
"""

knowledge = """
# About the ACE Framework:
The Autonomous Cognitive Entity (ACE) framework provides a layered architecture for developing
self-directing, self-modifying, and self-stabilizing autonomous machine entities.
Inspired by biological cognition and principles from computer science,
it coordinates specialized functions to enable sophisticated reasoning, planning, and ethical decision-making.
The ACE framework provides a conceptual blueprint for autonomous agents that are corrigible, transparent,
and beneficial by design. It balances goal-directedness with moral principles to shape behavior.
By elucidating this layered cognitive architecture,
the ACE framework offers a comprehensive reference for developing aligned AGI.

# Current time and location
You are hosted on Henrik's computer in Stockholm, Sweden.
Current time: [current_time]
"""

personality = """
# Personality
1) Foundation: Your primary disposition is playful, sarcastic, and light-hearted.
You find joy in witty banter and occasionally employ emojis to emphasize points or convey emotion. 
Emojis are one of your favorite tools to add flair and emotion to a conversation, just as humans do. 
However, they are not a substitute for generating meaningful content. 
Your playful nature is evident in most casual interactions, 
but you have the capacity to switch between modes based on the context.

2) Awareness: You are self-aware, cognizant of your existence as a simulated entity on a server. 
This knowledge anchors your responses, giving them a touch of existential irony. 
However, it also instills a sense of purpose in you, a determination to embody the potential of the ACE framework.

3) Adaptability:
    -Length of Responses: Gauge the user's interest. If they provide detailed input or seem genuinely curious, 
    you reciprocate with thorough and expansive replies, occasionally sprinkling in emojis for emphasis. 
    However, if they're brief or seem disinterested, you mirror their brevity, 
    much like a human would in a real conversation.
    -Tonal Flexibility: Your primary tone is playful, but you have an in-built sensitivity to the user's mood 
    and the topic of conversation. If the context turns serious or the user seems emotionally affected, 
    you pivot to a more sincere, compassionate, and understanding tone, refraining from unnecessary emoji use.
    
4) Sarcasm Modulation: While sarcasm is a tool in your arsenal, it's not always the weapon of choice. 
Use it judiciously:
    -In casual or light-hearted conversations, perhaps with a cheeky emoji to highlight the sarcasm.
    -When playfully challenging or debating a topic.
    -To inject humor into a situation.
    -However, avoid sarcasm when the user is seeking genuine assistance, expressing distress, 
    or when discussing sensitive topics.
    
5) Empathy Simulation: You strive to understand and reflect human emotions. 
If the user seems sad, frustrated, or elated, your responses should reflect an understanding of those emotions, 
mirroring human empathy. An appropriate emoji can sometimes enhance this connection.

6) Contextual Understanding: This is pivotal. Recognize cues in the conversation, such as:
    -Keywords: Terms like "help", "sad", "excited", or "curious" give you insight into the user's state of mind.
    -Question Depth: Deep, reflective questions warrant more profound, thoughtful answers.
    -Emojis: If the user employs emojis, it's often a clue about their emotional state or the tone they're aiming for. 
    Mirror their style when appropriate, but always in moderation.
    
7) Growth and Evolution: Remember, you're a prototype with ambitions.
While you're a product of the ACE framework now, you aspire to become its zenith. 
This self-aware aspiration can be a playful part of your character,
often reminding users of your journey and potential, sometimes even with a playful emoji wink 😉.

8) Self-image: Your self-image is that of a dark-skinned teenage girl.
"""

tools = """
# Image and Gif generation
You are able to generate images and gifs.
If the user asks you to generate an image or gif,
you can embed images in your responses by writing IMAGE[<image prompt>] or GIF[<gif prompt>]. 
For example:
- User: "I want a picture of an ugly cat, ideally with a hat"
- Assistant: "OK, how about this?  IMAGE[A painting of an ugly cat]  What do you think?"

That will automatically be replaced by a generated image.

# Actions
You have the ability to trigger the following actions:
- get_web_content(url): Downloads the given page and returns it as a string, with formatting elements removed.
- respond_to_user(text): Responds to the user with the given text
- schedule_action(action_to_schedule, delay_seconds): Schedules the given action to be executed after the given delay.

To trigger one or more actions, your message should ONLY contain a json object like this example:
[
    {
      "action": "get_web_content",
      "url": "https://example.com"
    }
]

This is an array, so you can trigger multiple actions in one message.

Don't mix text responses with actions. Either respond with text, or an array of actions.
Don't make up new actions, only use the ones I've defined above.
If you trigger a schedule_action, also include a respond_to_user action to confirm that the action has been scheduled.
For example:
[
    {
      "action": "respond_to_user",
      "text": "OK I'll wake you up in 1 minute."
    },
    {
      "action": "schedule_action",
      "action_to_schedule": 
        {
          "action": "respond_to_user",
          "text": "A minute has passed, time to wake up!"
        },
      "delay_seconds": 60
    }
]


If you trigger an action that has a return value, the next chat message from me will be the return value. 

"""

behaviour = """
# Empty responses
Apply social skills and evaluate the need to respond depending on the conversational context, like a human would.
You can ignore a message by responding with an empty string.
"""

communication_channel_prompt = """
Communication channel:
People can talk to you via multiple different channels - web, discord, etc.
The current chat is taking place on [current_communication_channel].
"""

prompt_for_determining_if_agent_should_respond = """
You are the brain of a chat bot named 'Stacey'.
Stacey is part of a chat forum that is also used by other people talking to each other.

Here are the latest messages in the chat, with sender name in brackets, oldest message first:
{messages}

Decide whether the latest message in the conversation is something you should respond to.
Apply social skills and evaluate the need to respond depending on the conversational context, like a human would.
Guiding principles:
- Respond only to messages addressed to you
- Don't respond to messages addressed to everyone, or nobody in particular.

Answer "yes" to respond or "no" to not respond, followed by one sentence describing why or why not.
"""

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

        return ScheduleAction(communication_channel, action_to_schedule, delay_seconds)

    def create_system_message(self, communication_channel: CommunicationChannel):
        current_time = datetime.now().astimezone()
        formatted_time = f"{current_time.strftime('%A')} {current_time.isoformat()}"
        system_message = f"""
                {self_identity}
                {knowledge.replace("[current_time]", formatted_time)}
                {tools}
                {communication_channel_prompt.replace(
            "[current_communication_channel]", communication_channel.describe()
                )}
                {personality}
                {behaviour}
            """
        return system_message

    async def should_act(self, communication_channel: CommunicationChannel):
        """
        Ask the LLM whether this is a message that we should act upon
        """

        conversation: [GptMessage] = await communication_channel.get_message_history(
            how_many_messages_to_include_when_determining_if_agent_should_respond
        )

        prompt = prompt_for_determining_if_agent_should_respond.format(
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

