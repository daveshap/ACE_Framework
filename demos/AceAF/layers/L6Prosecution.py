import re
from .AceLayer import AceLayer
from .customagents.l6prosecution.TaskProsecution import TaskProsecution


class L6Prosecution(AceLayer):

    def initialize_agents(self):
        self.agent = TaskProsecution()

    def parse_agent_output(self):
        # Define a regular expression pattern to match attribute names followed by their content
        pattern = r'(\w+):\s+("(.*?)"|None)'
        # Find all matches using the pattern
        matches = re.findall(pattern, self.my_messages['SouthBus'])

        # Convert matches to a dictionary
        parsed_data = {}
        for match in matches:
            key = match[0]
            # Check if the value is "None" or a string; if it's a string, we remove the quotes
            value = None if match[1] == "None" else match[2]
            parsed_data[key] = value

        self.interface.handle_south_bus(parsed_data)
