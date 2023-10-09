from agentforge.agent import Agent


class ExecutiveFunction(Agent):
    def load_additional_data(self):
        self.data['response_format'] = self.agent_data['settings']['directives'].get('ResponseFormat', None)
        self.data['southbound_format'] = self.agent_data['settings']['directives'].get('SouthboundFormat', None)
        self.data['northbound_format'] = self.agent_data['settings']['directives'].get('NorthboundFormat', None)
        self.data['format_note'] = self.agent_data['settings']['directives'].get('FormatNote', None)
