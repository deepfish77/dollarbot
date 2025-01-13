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
    INITIALIZED = "Payment Initialized"
    REJECTED_PAYMENT = "Payment rejected by provider"
    PAYMENT_SUCCESSFUL = "Payment completed succesfully"
    ORDER_RECEIVED_BY_BOT = "Service received the order"
    ORDER_COMPLETED_BY_BOT = "Service completed functionality"
    VERIFIED_OUTPUT = "Output was successfully saved to s3"
    BOT_FAILURE = "Bot failed to provide output to s3"
    REFUNDED = "Payment refunded to customer"
    CANCELLED = "User Cancelled transaction"

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

class TransferStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"
    REVERSED = "reversed"
    ON_HOLD = "on_hold"
    REFUNDED = "refunded"