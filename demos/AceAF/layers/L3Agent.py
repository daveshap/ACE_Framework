from .AceLayer import AceLayer
from .customagents.l3agent.SelfModel import SelfModel


class L3Agent(AceLayer):

    def initialize_agents(self):
        self.agent = SelfModel()





