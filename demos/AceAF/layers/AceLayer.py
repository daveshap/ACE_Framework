from . import LAYER_REGISTRY
from agentforge.utils.storage_interface import StorageInterface
import threading
from agentforge.config import Config
from .Interface import Interface
import time


class AceLayer:

    def __init__(self):
        self.layer_name = self.__class__.__name__
        self.layer_number = int(self.layer_name[1])  # Strip the 'L' prefix and layer name to get the number
        self.north_layer = self.layer_number - 1
        self.south_layer = self.layer_number + 1

        self.storage = StorageInterface().storage_utils
        self.config = Config()
        self.interface = Interface()

        self.bus = {'NorthBus': None, 'SouthBus': None}

        self.events = []
        self.north_bus_update_event = threading.Event()
        self.south_bus_update_event = threading.Event()
        self.input_update_event = threading.Event()
        self.user_update_event = threading.Event()

        self.result = "Just a testo"

        LAYER_REGISTRY[self.layer_number] = self

    def stand_by(self):
        # Clear old threads
        self.events.clear()

        # Create new threads for each event
        self.events.append(
            self.create_event_thread('North Bus', self.north_bus_update_event, self.handle_north_bus_update))
        self.events.append(
            self.create_event_thread('South Bus', self.south_bus_update_event, self.handle_south_bus_update))
        self.events.append(self.create_event_thread('Input', self.input_update_event, self.handle_input_update))
        self.events.append(self.create_event_thread('User', self.user_update_event, self.handle_user_update))

    def run(self):
        self.interface.output_message(self.layer_number, "Hello")
        # self.update_bus(bus="NorthBus", message="Hello North Bus")
        self.load_data_from_bus(bus="NorthBus")
        self.load_data_from_bus(bus="SouthBus")

        self.process_data_from_buses()

        self.load_relevant_data_from_memory()
        self.run_agents()

        self.update_bus(bus="SouthBus", message=self.result)
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
        # Call individual Agents From Each Layer
        pass

    def create_event_thread(self, event_name, event, callback):
        def event_loop():
            while True:
                event.wait()
                callback()
                event.clear()

        self.interface.output_message(self.layer_number, f"{self.layer_name} - Listening to {event_name}!!!")

        thread = threading.Thread(target=event_loop)
        thread.daemon = True
        thread.start()
        return thread

    def update_bus(self, **kwargs):
        params = {
            'collection_name': kwargs['bus'],
            'ids': [self.layer_number.__str__()],
            'data': [kwargs['message']]
        }

        self.interface.output_message(self.layer_number, f"Saved To Bus:{kwargs['bus']}\nData:{kwargs['message']}\n")
        self.storage.save_memory(params)

        # if kwargs['bus'] == 'SouthBus' and self.south_layer < 7:
        #     LAYER_REGISTRY[self.south_layer].input_update_event.set()

    def load_data_from_bus(self, **kwargs):  # North Bus
        bus_name = kwargs['bus']
        params = {"collection_name": bus_name}
        self.bus[bus_name] = self.storage.load_collection(params)
        # self.interface.output_message(self.layer_number, f"Loaded Data:{self.bus[bus_name]}\n")

    def load_relevant_data_from_memory(self):
        # Load Relevant Memories
        pass

    def process_data_from_buses(self):
        # for bus, data in self.bus.items():
        #     self.interface.output_message(self.layer_number, f"\nBus:{bus}\nData:{data}\n")
            # this may be overriden by each layer, maybe we add a function here specifically for overriding
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
