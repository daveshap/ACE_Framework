from actions.action import Action

from memory.weaviate_memory_manager import WeaviateMemoryManager


class GetAllMemories(Action):
    def __init__(self, memory_manager: WeaviateMemoryManager):
        self.memory_manager = memory_manager

    async def execute(self):
        print("Retrieving all memories")
        memories = self.memory_manager.get_all_memories()
        return "\n".join(f"- <{memory['time_utc']}>: {memory['content']}" for memory in memories)

    def __str__(self):
        return "Get all memories "



