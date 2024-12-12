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
