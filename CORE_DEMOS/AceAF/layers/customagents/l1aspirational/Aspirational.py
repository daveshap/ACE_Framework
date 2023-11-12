from agentforge.agent import Agent


class Aspirational(Agent):

    def load_additional_data(self):
        self.data['response_format'] = self.agent_data['settings']['directives'].get('ResponseFormat', None)
        self.data['southbound_format'] = self.agent_data['settings']['directives'].get('SouthboundFormat', None)
        self.data['northbound_format'] = self.agent_data['settings']['directives'].get('NorthboundFormat', None)
        self.data['format_note'] = self.agent_data['settings']['directives'].get('FormatNote', None)
        self.data['mission'] = self.agent_data['settings']['directives'].get('Mission', None)
        self.data['udhr'] = self.agent_data['settings']['directives'].get('UDHR', None)
        self.data['heuristics'] = self.agent_data['settings']['directives'].get('Heuristics', None)

        if not self.data['bottom_message']:
            self.data['bottom_message'] = self.agent_data['settings']['directives'].get('Situation', None)