from .AceLayer import AceLayer
from .customagents.l6prosecution.TaskProsecution import TaskProsecution


class L6Prosecution(AceLayer):

    def initialize_agents(self):
        self.agent = TaskProsecution()
