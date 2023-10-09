import re
from .AceLayer import AceLayer
from .customagents.l6prosecution.TaskProsecution import TaskProsecution


class L6Prosecution(AceLayer):

    def initialize_agents(self):
        self.agent = TaskProsecution()

    def parse_agent_output(self):
        # Define a regular expression pattern to match attribute names followed by their content
        pattern = r'(\w+):\s+("(.*?)"|None)'

        def parse_message(message):
            # Find all matches using the pattern
            matches = re.findall(pattern, message)

            # Convert matches to a dictionary
            parsed_data = {}
            for match in matches:
                key = match[0]
                # Check if the value is "None" or a string; if it's a string, we remove the quotes
                value = None if match[1] == "None" else match[2]
                parsed_data[key] = value

            return parsed_data

        south_bus_data = parse_message(self.my_messages['SouthBus'])
        north_bus_data = parse_message(self.my_messages['NorthBus'])

        # Merge the parsed data from both buses into one dictionary
        combined_data = {**south_bus_data, **north_bus_data}

        self.interface.handle_south_bus(combined_data)
