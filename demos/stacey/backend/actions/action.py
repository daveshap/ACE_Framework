from abc import ABC, abstractmethod
from typing import Optional


class Action(ABC):
    @abstractmethod
    async def execute(self) -> Optional[str]:
        """
        Executes the given action.
        If it returns a string, that string will be sent back to the LLM for further processing.
        If it doesn't return anything, then the action is considered to be a "fire and forget" action.
        """
        pass
