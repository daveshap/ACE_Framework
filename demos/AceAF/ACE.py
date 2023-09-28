from agentforge.utils.storage_interface import StorageInterface
from layers.L1Aspirational import L1Aspiration
from layers.L2Strategy import L2Strategy
from layers.L3Agent import L3Agent
from layers.L4Executive import L4Executive
from layers.L5Cognitive import L5Cognitive
from layers.L6Prosecution import L6Prosecution
from layers.Interface import Interface


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

        # self.layers[1].stand_by()
        # Load Immutable Data for L1 (Constitution/Heuristics/Mission)


if __name__ == '__main__':
    ACE().run()
