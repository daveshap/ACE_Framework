# l2_global_strategy.py
from .ace_layer import AceLayer
from .bus import Bus

from ..llm.gpt import GPT  # Hardcode to GPT for now


class L5CognitiveControlLayer(AceLayer):
    """
    The Cognitive Control Layer is responsible for dynamic task switching and selection based on environmental
    conditions and progress toward goals. It chooses appropriate tasks to execute based on project plans from the
    Executive Function Layer.
    """

    def __init__(self, llm: GPT, model,
                 southbound_bus: Bus, northbound_bus: Bus):
        super().__init__(5)
        self.llm = llm
        self.model = model
        self.southbound_bus = southbound_bus
        self.northbound_bus = northbound_bus
        self.beliefs = ""

    def on_northbound_message(self, message):
        self.process_input(message)

    def process_input(self, message):
        pass

    def send_southbound_message(self, message):
        self.log("Sending south: " + message)
        self.southbound_bus.publish(self.get_name(), message)

