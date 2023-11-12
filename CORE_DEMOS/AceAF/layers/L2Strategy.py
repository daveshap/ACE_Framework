from .AceLayer import AceLayer
from .customagents.l2strategy.GlobalStrategy import GlobalStrategy


class L2Strategy(AceLayer):
    def initialize_agents(self):
        self.agent = GlobalStrategy()
