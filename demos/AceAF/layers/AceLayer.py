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
        self.top_layer_message = None
        self.my_message = None
        self.bottom_layer_message = None

        self.events = []
        self.north_bus_update_event = threading.Event()
        self.south_bus_update_event = threading.Event()
        self.input_update_event = threading.Event()
        self.user_update_event = threading.Event()

        self.result = None

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
        self.interface.output_message(self.layer_number, f"\n------Running {self.layer_name} ------\n")
        # self.update_bus(bus="NorthBus", message="Hello North Bus")
        # self.load_data_from_bus(bus="NorthBus")
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

        # self.interface.output_message(self.layer_number, f"{self.layer_name} - Listening to {event_name}!!!")

        thread = threading.Thread(target=event_loop)
        thread.daemon = True
        thread.start()
        return thread

    def update_bus(self, **kwargs):
        self.my_message = kwargs['message'].__str__()

        params = {
            'collection_name': kwargs['bus'],
            'ids': [self.layer_number.__str__()],
            'data': [self.my_message]
        }

        self.storage.save_memory(params)

        if kwargs['bus'] == 'SouthBus' and self.south_layer < 7:
            LAYER_REGISTRY[self.south_layer].input_update_event.set()

        self.interface.output_message(self.layer_number, f"\n{self.my_message}\n")

    def load_data_from_bus(self, **kwargs):  # North Bus
        bus_name = kwargs['bus']
        params = {"collection_name": bus_name}
        self.bus[bus_name] = self.storage.load_collection(params)
        # self.interface.output_message(self.layer_number, f"Loaded Data:{self.bus[bus_name]}\n")

    def load_relevant_data_from_memory(self):
        # Load Relevant Memories
        pass

    def process_data_from_buses(self):
        # self.interface.output_message(0, self.bus.__str__())
        # print(self.bus.__str__())
        # north_bus = self.bus.get("NorthBus", None)
        south_bus = self.bus.get("SouthBus", None)

        north_layer = self.north_layer.__str__()
        south_layer = self.south_layer.__str__()

        # North Layer Writes to South Bus, Hence it's a Message from the Top Layer
        if north_layer in south_bus['ids']:
            index = south_bus['ids'].index(north_layer)
            self.top_layer_message = south_bus['documents'][index]

        # self.interface.output_message(self.layer_number, f"North Incoming Message:\n{self.top_layer_message}\n")

        # # North Layer Writes to South Bus, Hence it's a Message from the Bottom Layer
        # if south_layer in north_bus['ids']:
        #     index = north_bus['ids'].index(north_layer)
        #     self.bottom_layer_message = north_bus['documents'][index]

    def handle_north_bus_update(self, text):
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
