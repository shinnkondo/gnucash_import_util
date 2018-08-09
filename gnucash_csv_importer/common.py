import typing
import datetime
from gnucash_csv_importer.account import Account

class PartialTransactionInfo(typing.NamedTuple):
    date: datetime.date
    description: str
    deposit: int

class TransactionInfo(typing.NamedTuple):
    date: datetime.date
    description: str
    deposit: int
    account: Account