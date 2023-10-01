from .AceLayer import AceLayer
from .StrategyUpdateAgent import StrategyUpdateAgent


class L2Strategy(AceLayer):

    agent = StrategyUpdateAgent()
    layer1text = None
    layer3text = None

    def load_relevant_data_from_memory(self):
        self.interface.output_message(0, self.bus.__str__())
        print(self.bus.__str__())
        if '1' in self.bus['SouthBus']['ids']:
            index = self.bus['SouthBus']['ids'].index('1')
            self.layer1text = self.bus['SouthBus']['documents'][index]
        if '3' in self.bus['NorthBus']['ids']:
            index = self.bus['NorthBus']['ids'].index('3')
            self.layer3text = self.bus['NorthBus']['documents'][index]



    def run_agents(self):
        print(f"\nLayer 1: {self.layer1text}\nLayer 3: {self.layer3text}")
        testo = self.agent.run(agentlayer=f"{self.layer1text}\n\n{self.layer3text}")
        self.update_bus(bus="SouthBus", message=testo)
        self.update_bus(bus="NorthBus", message=testo)
        self.interface.output_message(self.layer_number, testo)
