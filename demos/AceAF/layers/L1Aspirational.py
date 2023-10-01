from .AceLayer import AceLayer
from agentforge.config import Config
from .customagents.l1aspirational.L1Default import L1Default


class L1Aspirational(AceLayer):

    constitution = None
    environment = None
    l1_agent = L1Default()

    def load_relevant_data_from_memory(self):
        # Load Relevant Memories
        self.constitution = self.config.data['Constitution']

    def run_agents(self):
        self.result = self.l1_agent.run(constitution=self.constitution, strategy_layer=self.bottom_layer_message)
        self.update_bus(bus="SouthBus", message=self.result)
        self.interface.output_message(self.layer_number, self.result)
        # self.update_bus(bus="SouthBus", message=testo)



