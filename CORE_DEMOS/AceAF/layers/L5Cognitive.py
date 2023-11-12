from .AceLayer import AceLayer
from .customagents.l5cogntiive.CognitiveControl import CognitiveControl


class L5Cognitive(AceLayer):

    def initialize_agents(self):
        self.agent = CognitiveControl()
