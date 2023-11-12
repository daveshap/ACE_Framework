from abc import ABC
from typing import Callable

from ace.types import LayerState

# Used when removing memories. Lower number means we will be more picky about only removing closely matching memories.
remove_memory_max_distance = 0.1


class AceLayer(ABC):
    """Superclass for all layers"""
    def __init__(self, layer_id: str):
        self.layer_id = layer_id
        self.layer_state_listeners = set()

    def get_name(self):
        return self.__class__.__name__

    def get_id(self):
        return self.layer_id

    def add_layer_state_listener(self, listener: Callable[[LayerState], None]):
        self.layer_state_listeners.add(listener)

    def remove_layer_state_listener(self, listener: Callable[[LayerState], None]):
        self.layer_state_listeners.discard(listener)

    async def notify_layer_state_subscribers(self):
        layer_state = self.get_layer_state()
        for listener in self.layer_state_listeners:
            await listener(layer_state)

    def get_layer_state(self) -> LayerState:
        """Returns the current state of the layer as a dictionary. For use by admin web and similar. """
        pass

    def log(self, message):
        print(f"{self.get_name()}: {message}")
