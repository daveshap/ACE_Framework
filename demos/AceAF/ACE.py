import threading
from layers.L1Aspirational import L1Aspiration
from layers.L2Strategy import L2Strategy


class ACE:

    def __init__(self):
        self.l1 = L1Aspiration()
        self.l2 = L2Strategy()
        self.l3 = None
        self.l4 = None
        self.l5 = None
        self.l6 = None

    def run(self):
        self.l1.start()
        pass

