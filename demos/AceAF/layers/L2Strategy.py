from .AceLayer import AceLayer
from .customagents.l2strategy.StrategyUpdateAgent import StrategyUpdateAgent


class L2Strategy(AceLayer):

    strategy = StrategyUpdateAgent()

    def run_agents(self):
        self.result = self.strategy.run(top_message=self.top_layer_message,
                                        bottom_message=self.bottom_layer_message,
                                        self_message=self.my_message)
