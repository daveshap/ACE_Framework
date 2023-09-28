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


class ACE:

    def __init__(self):
        self.storage = StorageInterface().storage_utils
        self.io = Interface()

        # Initializing layers
        self.layers = {
            1: L1Aspiration(),
            2: L2Strategy(),
            3: L3Agent(),
            4: L4Executive(),
            5: L5Cognitive(),
            6: L6Prosecution()
        }

    def run(self):
        # Sequentially set layers on stand_by
        for layer_number in sorted(self.layers.keys()):
            self.layers[layer_number].stand_by()

        print("\nAll Layers Initialized, ACE Running...\n")

        # Main loop
        while True:
            # Check for 'ESC' key press
            if keyboard.is_pressed('esc'):
                print("Escape key detected! Exiting...")
                break

            for layer_number, layer_instance in self.layers.items():
                for thread_info in layer_instance.threads:
                    # Check if the thread is not alive
                    if not thread_info['thread'].is_alive():
                        print(f"Thread with UID {thread_info['uid']} from {layer_instance.layer_name} has stopped!")
                        # Reinitialize the layer
                        layer_instance.stand_by()

            # Sleep for some time (e.g., 1 second) before checking again
            time.sleep(1)


if __name__ == '__main__':
    ACE().run()
