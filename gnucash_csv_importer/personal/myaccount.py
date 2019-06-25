from enum import auto

from gnucash_csv_importer.account import Account

class MyAccount(Account):
    CARD = auto()
    TRANSPORTATION = auto()
    MEALS = auto()
    SNACK = auto()
    SUICA = auto()
    SMBC_CARD_AMAZON = auto()
    SMBC_CARD_OTHERS = auto()
    LINE_PAY = auto()
    JP_BANK = auto()
    UNKNOWN = auto()