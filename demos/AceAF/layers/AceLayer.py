from threading import Event

from . import LAYER_REGISTRY
from agentforge.utils.storage_interface import StorageInterface
import threading
from agentforge.config import Config
from demos.AceAF.guiutils.sendtoui import ApiClient

# def get_layer_by_number(layer_number):
#     return LAYER_REGISTRY.get(layer_number, None)


class AceLayer:

    def __init__(self):
        self.layer_name = self.__class__.__name__
        self.layer_number = int(self.layer_name[1])  # Strip the 'L' prefix and layer name to get the number
        self.north_layer = self.layer_number - 1
        self.south_layer = self.layer_number + 1

        self.storage = StorageInterface().storage_utils
        self.config = Config()

        self.events = []
        self.north_bus_update_event = threading.Event()
        self.south_bus_update_event = threading.Event()
        self.input_update_event = threading.Event()
        self.user_update_event = threading.Event()
        self.sendui = ApiClient()

        self.result = None

        LAYER_REGISTRY[self.layer_number] = self

    def stand_by(self):
        # Clear old threads
        self.events.clear()

        # Create new threads for each event
        self.events.append(self.create_event_thread('North Bus', self.north_bus_update_event, self.handle_north_bus_update))
        self.events.append(self.create_event_thread('South Bus', self.south_bus_update_event, self.handle_south_bus_update))
        self.events.append(self.create_event_thread('Input', self.input_update_event, self.handle_input_update))
        self.events.append(self.create_event_thread('User', self.user_update_event, self.handle_user_update))

    def run(self):
        print(f"\n\n{self.layer_name} Ran!!!\n\n")
        self.sendui.send_message("api1", "Hello")
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

    def run_agents(self):
        # Call individual Agents
        pass

    def create_event_thread(self, event_name, event, callback):
        def event_loop():
            while True:
                event.wait()
                callback()
                event.clear()

        print(f"{self.layer_name} - Listening to {event_name}!!!")
        self.sendui.send_message(self.layer_name, f"{self.layer_name} - Listening to {event_name}!!!")

        thread = threading.Thread(target=event_loop)
        thread.daemon = True
        thread.start()
        return thread

    def update_south_bus(self):
        params = {}
        self.storage.save_memory(params)
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

    def handle_north_bus_update(self):
        # Load Data From North Bus and process
        self.run()

    def handle_south_bus_update(self):
        # Load Data From South Bus and process
        self.run()

    def handle_input_update(self):
        # Load Relevant Data From Input and process
        self.run()

    def handle_user_update(self):
        # Load Relevant Data From Input and process
        self.run()


