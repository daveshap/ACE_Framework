from .AceLayer import AceLayer
from agentforge.config import Config
from .TestAgent import TestAgent

class L1Aspirational(AceLayer):

    constitution = None
    environment = None
    agent = TestAgent()

    def load_relevant_data_from_memory(self):
        # Load Relevant Memories
        self.constitution = self.config.data['Constitution']
        # self.interface.output_message(0, self.bus.__str__())

        try:
            self.environment = self.bus['NorthBus']['id':2]
        except:
            pass

    def run_agents(self):
        testo = self.agent.run(constitution=self.constitution, strategylayer=self.environment)
        self.update_bus(bus="SouthBus", message=testo)
        self.interface.output_message(self.layer_number, testo)
        # self.update_bus(bus="SouthBus", message=testo)



