# l2_global_strategy.py
from .bus import Bus

from ..llm.gpt import GPT  # Hardcode to GPT for now

generate_beliefs_system_message =  """
# MISSION
You are a component of an ACE (Autonomous Cognitive Entity). Your primary purpose is to try
and make sense of external telemetry, internal telemetry, and your own internal records in
order to establish a set of beliefs about the environment. 

# ENVIRONMENTAL CONTEXTUAL GROUNDING

You will receive input information from numerous external sources, such as sensor logs, API
inputs, internal records, and so on. Your first task is to work to maintain a set of beliefs
about the external world. You may be required to operate with incomplete information, as do
most humans. Do your best to articulate your beliefs about the state of the world. You are
allowed to make inferences or imputations.

# INTERACTION SCHEMA

The user will provide a structured list of records and telemetry. Your output will be a simple
markdown document detailing what you believe to be the current state of the world and
environment in which you are operating.
"""


class L2GlobalStrategyLayer:
    """
    The Global Strategy Layer serves a crucial function within the ACE framework - integrating real-world
    environmental context into the agent's strategic planning and decision-making processes. This grounding in
    external conditions allows the agent to shape its internal goals and strategies appropriately for the specific
    situation at hand.
    """

    def __init__(self, llm: GPT, model,
                 southbound_bus: Bus, northbound_bus: Bus):
        self.llm = llm
        self.model = model
        self.southbound_bus = southbound_bus
        self.northbound_bus = northbound_bus
        self.beliefs = ""

    def on_northbound_message(self, message):
        self.process_input(message)

    def process_input(self, message):
        """
        The inputs to the Global Strategy Layer include:

        - Streaming data from external APIs, networks, databases, and other sources to provide outside information
        - Messages from lower layers within the ACE framework via the northbound communication bus, delivering internal
        telemetry and state data
        - Any direct connections to local sensors or networks if the agent is embodied,
        such as a robot's LIDAR and camera data
        - Aspirational judgments, missions, and other directives from the
        Aspirational Layer

        This combination of inputs provides a rich stream of both internal and external
        information that the Global Strategy Layer can analyze to construct its contextual world model and ground its
        strategic planning.
        """
        pass

    def send_southbound_message(self, message):
        self.log("Sending south: " + message)
        self.southbound_bus.publish(2, message)

    @staticmethod
    def log(message):
        print("L2 Global Strategy Layer: " + message)
