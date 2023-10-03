from typing import Callable

from ace.layer_status import LayerStatus


class AceLayer:
    """Superclass for all layers"""
    def __init__(self):
        self.status: LayerStatus = LayerStatus.IDLE
        self.status_listeners = set()

    def get_name(self):
        return self.__class__.__name__

    def set_status(self, status: LayerStatus):
        print(f"{self.get_name()} status changed to {status}. Notifying {len(self.status_listeners)} listeners.")
        self.status = status
        for listener in self.status_listeners:
            listener(self.status)

    def add_status_listener(self, listener: Callable[[LayerStatus], None]):
        self.status_listeners.add(listener)

    def remove_status_listener(self, listener: Callable[[LayerStatus], None]):
        self.status_listeners.discard(listener)

    def log(self, message):
        print(f"{self.get_name()}: {message}")