from .AceLayer import AceLayer
from agentforge.config import Config
from .customagents.l1aspirational.L1Default import L1Default


class L1Aspirational(AceLayer):

    l1_agent = L1Default()

    def run_agents(self):
        self.result = self.l1_agent.run(bottom_message=self.bottom_layer_message,
                                        self_message=self.my_message)



