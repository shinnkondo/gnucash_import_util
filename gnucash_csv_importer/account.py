from enum import Enum, auto

class Account(Enum):
    CARD = auto()
    TRANSPORTATION = auto()
    MEALS = auto()
    SNACK = auto()
    SUICA = auto()
    UNKNOWN = auto()