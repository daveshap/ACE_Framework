from agentforge.utils.storage_interface import StorageInterface
from layers.L1Aspirational import L1Aspiration
from layers.L2Strategy import L2Strategy
from layers.L3Agent import L3Agent
from layers.L4Executive import L4Executive
from layers.L5Cognitive import L5Cognitive
from layers.L6Prosecution import L6Prosecution
from layers.Interface import Interface

import time
import keyboard

import threading


class ACE:

    def __init__(self):
        self.storage = StorageInterface().storage_utils
        self.io = Interface()
        self.layer_threads = {}

        # Initializing layers
        self.layers = {
            1: L1Aspiration(),
            2: L2Strategy(),
            3: L3Agent(),
            4: L4Executive(),
            5: L5Cognitive(),
            6: L6Prosecution()
        }

        self.layer_threads = {}  # To hold the threads

        for layer_number, layer_instance in self.layers.items():
            thread = threading.Thread(target=layer_instance.stand_by)
            thread.daemon = True
            thread.start()

        print("\nAll Layers Initialized, ACE Running...\n")

    def run(self):
        # Trigger L1
        self.layers[1].input_update_event.set()

        # Main loop
        while True:
            # Check for 'ESC' key press
            if keyboard.is_pressed('esc'):
                print("Escape key detected! Exiting...")
                break

    def init_layer(self, layer_number):
        try:
            self.layers[layer_number].stand_by()
        except Exception as e:
            print(f"Error in layer {layer_number}: {e}")


if __name__ == '__main__':
    ACE().run()
