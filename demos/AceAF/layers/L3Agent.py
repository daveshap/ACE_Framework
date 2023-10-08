from .AceLayer import AceLayer
from .customagents.l3agent.SelfModel import SelfModel


class L3Agent(AceLayer):
    input_data = None

    def initialize_agents(self):
        self.agent = SelfModel()

    def load_relevant_data(self):
        self.interface.refresh_info()

        self.input_data = (f"Operating System Name: {self.interface.os_name}\n"
                           f"Operating System Version: {self.interface.os_version}\n"
                           f"System: {self.interface.system}\n"
                           f"Architecture: {self.interface.architecture}\n"
                           f"Current Date and Time: {self.interface.date_time}")

    def run_agents(self):
        # Call individual Agents From Each Layer
        self.result = self.agent.run(top_message=self.top_layer_message,
                                     bottom_message=self.bottom_layer_message,
                                     input_data=self.input_data)
