from .AceLayer import AceLayer
from agentforge.config import Config


class L1Aspirational(AceLayer):

    def run(self):
        constitution = self.config.data['Constitution']
        print(constitution)



