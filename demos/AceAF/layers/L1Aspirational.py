from .AceLayer import AceLayer
from agentforge.config import Config
from .customagents.l1aspirational.L1Default import L1Default


class L1Aspirational(AceLayer):

    l1_agent = L1Default()

    def load_relevant_data_from_memory(self):
        # Load Relevant Data
        self.l1_agent.data['mission'] = self.config.settings['directives']['Mission']
        self.l1_agent.data['udhr'] = self.config.settings['directives']['UDHR']
        self.l1_agent.data['heuristics'] = self.config.settings['directives']['Heuristics']
        self.l1_agent.data['situation'] = self.config.settings['directives']['Situation']

        if self.bottom_layer_message:
            self.l1_agent.data['situation'] = self.bottom_layer_message

    def run_agents(self):
        self.result = self.l1_agent.run()



