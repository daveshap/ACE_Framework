from enum import Enum


class OperationClassification(Enum):
    CREATE_REQUEST = "CREATE_REQUEST"
    ADD_TO_CONTEXT = "ADD_TO_CONTEXT"
    TAKE_ACTION = "TAKE_ACTION"
