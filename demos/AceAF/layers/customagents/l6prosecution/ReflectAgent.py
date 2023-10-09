from agentforge.agent import Agent


class ReflectAgent(Agent):

    def load_additional_data(self):
        self.data['persona_name'] = self.agent_data['persona']['Persona']['Name']
        self.data['persona_description'] = self.agent_data['persona']['Persona']['Description']
        self.data['persona_location'] = self.agent_data['persona']['Persona']['Location']
        self.data['persona_setting'] = self.agent_data['persona']['Persona']['Setting']
        self.data['persona_user'] = self.agent_data['persona']['Persona']['Username']
        self.data['Narrative'] = "none"
