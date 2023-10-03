from abc import abstractmethod, ABC
from typing import Dict, Any


class Tool(ABC):
    """
    Abstract base class for tools.
    """

    @abstractmethod
    def use_tool(self, params: Dict[str, Any]) -> str:
        """
        Abstract method to use the tool. Each derived class must implement this.

        Args:
        - params (Dict[str, Any]): Parameters required to use the tool.

        Returns:
        - Any: Return type is determined by the specific tool.
        """
        pass
