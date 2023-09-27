from agentforge.utils.storage_interface import StorageInterface
import threading


class AceLayer:

    def __init__(self):
        self.layer_name = self.__class__.__name__
        self.layer_number = int(self.layer_name[1:-1])  # Strip the 'L' prefix and layer name to get the number
        self.north_layer = self.layer_number - 1
        self.south_layer = self.layer_number + 1

        self.storage = StorageInterface().storage_utils
        self.threads = []

    def start(self):
        # Create a new thread for the first layer
        uid = 'unique ID'
        thread = threading.Thread(target=self.run)
        thread.start()

        new_thread = {'uid': uid, 'thread': thread}
        self.threads.append(new_thread)

    def run(self):
        # Load Data From North Bus
        # Load Data From South Bus
        # Load Relevant Data From Input
        # Load Relevant Data From Chat
        # Load Relevant Data From Memory
        # Parse Data
        # Agent Logic
        # Parse Results
        # Update North Bus
        # Update South Bus
        # Remove Thread from self.threads
        pass

    def run_agents(self):
        # Call individual Agents
        pass

    def load_data_from_north_layer(self):  # South Bus
        if self.north_layer == 0:  # Layer 1 has no Layer Above, i.e. Layer 0
            pass

        # Query the North Bus Collection for message from the Layer Above
        pass

    def load_data_from_south_bus(self):  # North Bus
        if self.north_layer == 7:  # Layer 6 has no Layer Below, i.e. Layer 7
            pass

        # Query the South Bus Collection for message from the Layer Below
        pass

    def load_relevant_data_from_input(self):
        # Load Any Telemetry
        pass

    def load_relevant_data_from_chat(self):
        # Load Chat History
        pass

    def load_relevant_data_from_memory(self):
        # Load Relevant Memories
        pass



