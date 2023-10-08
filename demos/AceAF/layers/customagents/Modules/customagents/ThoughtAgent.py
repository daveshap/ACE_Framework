from agentforge.agent import Agent


class ThoughtAgent(Agent):

    def load_additional_data(self):
        self.data['persona_name'] = self.agent_data['persona']['Persona']['Name']
        self.data['persona_description'] = self.agent_data['persona']['Persona']['Description']
        self.data['persona_location'] = self.agent_data['persona']['Persona']['Location']
        self.data['persona_setting'] = self.agent_data['persona']['Persona']['Setting']
        self.data['persona_user'] = self.agent_data['persona']['Persona']['Username']
        self.data['Narrative'] = "none"

    def parse_result(self):
        # Initialize an empty dictionary to store the parsed data
        parsed_data = {}
        current_heading = None
        current_value = []

        lines = self.result.strip().split('\n')

        def store_current_section():
            if current_heading:
                parsed_data[current_heading] = '\n'.join(current_value)

        for line in lines:
            line = line.strip()  # Remove leading/trailing spaces

            # Check if this line is a heading (ends with a colon)
            if line.endswith(':'):
                # Store the previous section (if any)
                store_current_section()

                # Extract the new heading
                current_heading = line[:-1]  # Remove the colon
                current_value = []  # Initialize a new value list
            else:
                # This line is part of the current section
                current_value.append(line)

        # Store the last section
        store_current_section()

        return parsed_data
