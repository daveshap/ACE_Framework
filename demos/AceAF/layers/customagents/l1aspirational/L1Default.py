from agentforge.agent import Agent


class L1Default(Agent):

    def load_additional_data(self):
        self.data['mission'] = self.agent_data['settings']['directives'].get('Mission', None)
        self.data['udhr'] = self.agent_data['settings']['directives'].get('UDHR', None)
        self.data['heuristics'] = self.agent_data['settings']['directives'].get('Heuristics', None)

        if self.data['bottom_message']:
            self.data['situation'] = self.data['bottom_message']

        if self.data['bottom_message']:
            self.data['situation'] = self.data['bottom_message']
            return

        self.data['situation'] = self.agent_data['settings']['directives'].get('Situation', None)




