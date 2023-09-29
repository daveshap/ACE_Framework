# ace/ace_system.py
from .bus import Bus
from .l1_aspirational import L1AspirationalLayer


class AceSystem:
    def __init__(self, llm, model):
        self.northbound_bus = Bus('northbound')
        self.southbound_bus = Bus('southbound')

        self.l1_aspirational_layer = L1AspirationalLayer(
            llm,
            model,
            self.southbound_bus,
            self.northbound_bus
        )

    def start(self):
        self.northbound_bus.subscribe(self.l1_aspirational_layer.on_northbound_message)
