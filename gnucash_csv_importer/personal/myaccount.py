from enum import Enum, auto


class MyAccount(Enum):
    CARD = auto()
    TRANSPORTATION = auto()
    MEALS = auto()
    SNACK = auto()
    SUICA = auto()
    UNKNOWN = auto()