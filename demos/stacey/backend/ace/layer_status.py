from enum import Enum, auto


class LayerStatus(Enum):
    IDLE = auto()
    INFERRING = auto()
