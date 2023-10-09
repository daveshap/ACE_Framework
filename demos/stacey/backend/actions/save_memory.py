from ace.types import create_memory
from actions.action import Action

from memory.weaviate_memory_manager import WeaviateMemoryManager


class SaveMemory(Action):
    def __init__(self, memory_manager: WeaviateMemoryManager, memory_string: str):
        self.memory_manager = memory_manager
        self.memory_string = memory_string

    async def execute(self):
        print("Saving memory: " + self.memory_string)
        self.memory_manager.save_memory(create_memory(self.memory_string))

    def __str__(self):
        return "Save memory: " + self.memory_string



