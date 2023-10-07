from .AceLayer import AceLayer
from .customagents.l4executive.TaskCreation import TaskCreation


class L4Executive(AceLayer):

    def initialize_agents(self):
        self.agent = TaskCreation()
