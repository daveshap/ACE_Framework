from enum import Enum


class MessageType(Enum):
    DATA = "DATA"
    PASS_THROUGH = "PASS_THROUGH"
    TELEMETRY = "TELEMETRY"
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    COMMAND = "COMMAND"
