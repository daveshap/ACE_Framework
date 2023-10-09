# ace/ace_system.py
from llm.gpt import GPT
from memory.weaviate_memory_manager import WeaviateMemoryManager
from .bus import Bus
from .l1_aspirational import L1AspirationalLayer
from .l2_global_strategy import L2GlobalStrategyLayer
from .l3_agent import L3AgentLayer


class AceSystem:
    def __init__(self, llm: GPT, model: str, memory_manager: WeaviateMemoryManager):
        self.northbound_bus = Bus('northbound')
        self.southbound_bus = Bus('southbound')

        self.l1_aspirational_layer: L1AspirationalLayer = L1AspirationalLayer()

        self.l2_global_strategy_layer: L2GlobalStrategyLayer = L2GlobalStrategyLayer(
            llm,
            model,
            memory_manager,
            self.l1_aspirational_layer
        )

        self.l3_agent: L3AgentLayer = L3AgentLayer(
            llm,
            model,
            memory_manager
        )

        self.layers = [
            self.l1_aspirational_layer,
            self.l3_agent
        ]

    def get_layer(self, layer_id: str):
        for layer in self.layers:
            if layer.get_id() == layer_id:
                return layer
        return None

    def get_layers(self):
        return self.layers

    async def start(self):
        # This would be the place for things like this:
        # self.northbound_bus.subscribe(self.l1_aspirational_layer.on_northbound_message)
        pass

