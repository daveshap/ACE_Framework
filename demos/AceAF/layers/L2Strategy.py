from .AceLayer import AceLayer
from .customagents.l2strategy.StrategyUpdateAgent import StrategyUpdateAgent


class L2Strategy(AceLayer):
    def initialize_agents(self):
        self.agent = StrategyUpdateAgent()
