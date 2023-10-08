from .AceLayer import AceLayer
from .customagents.l1aspirational.Aspirational import Aspirational


class L1Aspirational(AceLayer):

    def initialize_agents(self):
        self.agent = Aspirational()



