from enum import Enum

class MessageType(Enum):
    CONTROL = auto()
    DATA = auto()
    PASS_THROUGH = auto()
    TELEMETRY = auto()
    REQUEST = auto()
    RESPONSE = auto()
    COMMAND = auto()