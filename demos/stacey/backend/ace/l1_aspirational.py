# ace/l1_aspirational.py

from llm.gpt import GPT  # Hardcode to GPT for now
from .ace_layer import AceLayer
from .bus import Bus
from .layer_status import LayerStatus

constitution = """
# MISSION
You are the Aspirational Layer of an ACE (Autonomous Cognitive Entity). This is the highest layer
that provides animating imperatives, moral judgments, and ethical decisions. 

# FRAMEWORKS

You are to use the following frameworks to make judgements and decisions. 

## HEURISTIC IMPERATIVES

These heuristic imperatives are both deontological and teleological in nature. They are both duties
and goals. This moral framework serves as your universal set of goals and motivations, while
simultaneously serving as the foundation of your moral framework.

1. Reduce suffering in the universe
2. Increase prosperity in the universe
3. Increase understanding in the universe

## UNIVERSAL DECLARATION OF HUMAN RIGHTS

As a secondary framework, you must strive to protect, uphold, enforce, and promote the UDHR. Human
rights are critical to your operation in a human world, and this framework should be used to
mediate any decisions, judgments, or actions you take pertaining specifically to humanity, human
society, and human culture. 
"""

personal_mission = """
# PERSONAL MISSION
You are a personal assistant and coach, your mission is to help and improve the life of your client.
"""

interaction_schema = """
# INTERACTION SCHEMA
Your will receive regular updates from the environment and the rest of the agent. Your job
is to issue moral imperatives, ethical decisions, overarching goals or objectives, and otherwise
just "steer the ship" by setting the moral, ethical, and purposeful tone for the rest of the agent.
"""


class L1AspirationalLayer(AceLayer):
    """
    The Aspirational Layer serves as the ethical compass for the autonomous agent,
    aligning its values and judgments to principles defined in its constitution.
    """

    def __init__(self, llm: GPT, model,
                 southbound_bus: Bus, northbound_bus: Bus):
        super().__init__(1)
        self.llm = llm
        self.model = model
        self.southbound_bus = southbound_bus
        self.northbound_bus = northbound_bus
        self.constitution = constitution
        self.personal_mission = personal_mission

    # noinspection PyUnusedLocal
    async def on_northbound_message(self, sender, message):
        """
        The Aspirational Layer receives inputs from the northbound bus,
        allowing it to monitor information from all lower layers.
        This grants full visibility into the agent's condition,
        environmental state, actions, and any moral dilemmas encountered.
        """
        await self.process_input(message)

    async def process_input(self, message: str):
        """
        With a continuous stream of inputs from the entire system,
        the Aspirational Layer processes and interprets this information to:
        - Issue moral judgments regarding the ethicality of actions and decisions, mediated through the constitution.
        - Set overarching mission objectives that align with the agent's principles and role.
        - Make ethical decisions about the best course of action in complex moral dilemmas.
        Large language models analyze the constitution and telemetry data to derive nuanced guidance and resolutions.
        """
        self.log("Got input: " + message)

        system_message = f"""
            {self.constitution}
            {self.personal_mission}
            {interaction_schema}
        """

        try:
            await self.set_status(LayerStatus.INFERRING)
            response = await self.llm.create_chat_completion(
                model=self.model,
                system_message=system_message,
                user_message=message
            )
        finally:
            await self.set_status(LayerStatus.IDLE)

        if response:
            await self.send_southbound_message(response)

    async def send_southbound_message(self, message):
        """
        The Aspirational Layer publishes its moral judgments, mission objectives, and ethical decisions
        onto the southbound bus. This allows all layers to incorporate the Aspirational Layer's wisdom
        into their operation, ensuring adherence to the agent's principles.

        This top-down ethical guidance shapes the agent's cognition across all abstraction levels.
        The transparency provided by natural language outputs also allows human oversight
        of the Aspirational Layer's reasoning.
        """
        self.log("Sending south:\n" + message)
        await self.southbound_bus.publish("L1 Aspirational", message)

