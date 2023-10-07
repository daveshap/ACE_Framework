from .AceLayer import AceLayer
from agentforge.agents.SummarizationAgent import SummarizationAgent


class L3Agent(AceLayer):
    summarization = SummarizationAgent()

    def run_agents(self):
        self.result = self.summarization.run(text=self.top_layer_message)
