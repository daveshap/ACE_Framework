from agentforge.utils.storage_interface import StorageInterface
import threading


class AceLayer:

    def __init__(self):
        self.storage = StorageInterface().storage_utils
        self.threads = []

    def start(self):
        # Create a new thread for the first layer
        thread = threading.Thread(target=self.run)
        thread.start()

        # Optionally, you can keep track of threads if you need to join/wait for them later
        self.threads.append(thread)

    def run(self):
        # Load Data From South Bus
        # Load Data From North Bus
        # Do logic with data
        # Run Agents
        # Update South Bus
        # Update North Bus
        pass

    def RunAgents(self):
        # Call individual Agents
        # Deal with Results
        pass

