from .AceLayer import AceLayer
from .customagents.l5cogntiive.TaskSelectionAgent import TaskSelectionAgent


class L5Cognitive(AceLayer):

    def initialize_agents(self):
        self.agent = TaskSelectionAgent()
