# l2_global_strategy.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from llm.gpt import GPT
from .ace_layer import AceLayer
from .l1_aspirational import L1AspirationalLayer

client_agents = []

chat_history_length = 10


class L2GlobalStrategyLayer(AceLayer):
    def __init__(self, llm: GPT, model, memory_manager, l1_aspirational_layer: L1AspirationalLayer):
        super().__init__("2")
        self.llm = llm
        self.model = model
        self.l1_aspirational_layer = l1_aspirational_layer
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()


