from actions.action import Action
from memory.weaviate_memory_manager import WeaviateMemoryManager


class RemoveClosestMemory(Action):
    def __init__(self, memory_manager: WeaviateMemoryManager, memory_string: str, max_distance: float):
        self.memory_manager = memory_manager
        self.memory_string = memory_string
        self.max_distance = max_distance

    async def execute(self):
        print("Removing closest memory: " + self.memory_string)
        removed_memory = self.memory_manager.remove_closest_memory(self.memory_string, self.max_distance)
        if removed_memory is None:
            # Couldn't find a matching memory. The agent needs to know this, so it can inform the user
            return "No matching memory found"
        # Memory successfully removed. No need to return anything.

    def __str__(self):
        return "Remove closest memory: " + self.memory_string



