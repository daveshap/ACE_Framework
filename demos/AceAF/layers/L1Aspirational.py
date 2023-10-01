from .AceLayer import AceLayer
from agentforge.config import Config


class L1Aspirational(AceLayer):

    constitution = None

    def load_relevant_data_from_memory(self):
        # Load Relevant Memories
        self.constitution = self.config.data['Constitution']

    def run_agents(self):
        # Override Agents
        self.update_bus(bus="SouthBus", message=self.constitution)
        self.interface.output_message(self.layer_number, "TESTING RUN AGENT METHOD")



