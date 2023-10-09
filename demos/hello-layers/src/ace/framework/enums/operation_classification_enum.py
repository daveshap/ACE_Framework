from enum import Enum

class OperationClassification(Enum):
    CREATE_REQUEST = auto()
    ADD_TO_CONTEXT = auto()
    TAKE_ACTION = auto()