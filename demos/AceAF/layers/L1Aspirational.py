from .AceLayer import AceLayer
from .customagents.l1aspirational.L1Default import L1Default


class L1Aspirational(AceLayer):

    def initialize_agents(self):
        self.agent = L1Default()



