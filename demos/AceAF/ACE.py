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
        self.l1 = L1Aspiration()
        self.l2 = L2Strategy()
        self.l3 = L3Agent()
        self.l4 = L4Executive()
        self.l5 = L5Cognitive()
        self.l6 = L6Prosecution()
        self.io = Interface()

    def run(self):
        # Load Immutable Data for L1 (Constitution/Heuristics/Mission)
        # Start Initializing The Layers and Running them
        pass


