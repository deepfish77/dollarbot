from enum import Enum


class BOT_RETURN_TYPE(Enum):
    ON_SCREEN = "On Screen Result"
    FILE = "File Result"
    VIDEO = "Video Result"
    MULTIPLE_OBJECTS = "Multiple Objects"
    POSTPONED_RESULT = "Postponed result"
    THIRD_PARTY = "Third Party Result"

    def __init__(self, ui_val):
        self.ui_val = ui_val


class ORDER_STATUS(Enum):
    NEW = "New"
    STARTED = "Started"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    REFUNDED = "Refunded"

    def __init__(self, ui_val):
        self.ui_val = ui_val


class TRANSACTION_STATUS(Enum):
    INITIALIZED = "Initialized"
    BOT_EXECUTED = "Bot Executed"
    BOT_FAILED = "Bot Failed"
    COMPLETED = "Completed"
    PAYED = "Payed"
    REFUNDED = "Refunded"

    def __init__(self, ui_val):
        self.ui_val = ui_val
