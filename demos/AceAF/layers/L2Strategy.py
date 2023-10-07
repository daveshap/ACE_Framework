from .AceLayer import AceLayer
from .customagents.l2strategy.StrategyUpdateAgent import StrategyUpdateAgent


class L2Strategy(AceLayer):

    agent = StrategyUpdateAgent()

    def run_agents(self):
        self.result = self.agent.run(agentlayer=f"{self.top_layer_message}\n\n{self.bottom_layer_message}")
