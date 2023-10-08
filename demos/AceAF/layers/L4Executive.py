from .AceLayer import AceLayer
from .customagents.l4executive.ExecutiveFunction import ExecutiveFunction


class L4Executive(AceLayer):

    def initialize_agents(self):
        self.agent = ExecutiveFunction()
