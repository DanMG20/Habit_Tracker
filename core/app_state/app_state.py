from enum import Enum, auto

class AppMode(Enum):
    NORMAL = auto()
    ADD_HABIT = auto()
    MONTHLY_GRAPH = auto()
    YEARLY_GRAPH = auto()

class AppState:
    def __init__(self):
        self.mode = AppMode.NORMAL
