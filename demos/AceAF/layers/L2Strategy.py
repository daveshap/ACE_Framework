from .AceLayer import AceLayer
from ACE_Framework_AgentForge.demos.AceAF.layers.customagents.l2strategy.StrategyUpdateAgent import StrategyUpdateAgent


class L2Strategy(AceLayer):

    agent = StrategyUpdateAgent()

    def run_agents(self):
        # print(f"\nLayer 1: {self.layer1text}\nLayer 3: {self.layer3text}")
        self.result = self.agent.run(agentlayer=f"{self.top_layer_message}\n\n{self.bottom_layer_message}")
        self.update_bus(bus="SouthBus", message=self.result)
        self.update_bus(bus="NorthBus", message=self.result)
        self.interface.output_message(self.layer_number, self.result)
