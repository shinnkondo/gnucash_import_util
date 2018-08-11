import typing
import datetime
from gnucash_csv_importer.account import Account

class PartialTransactionInfo(typing.NamedTuple):
    date: datetime.date
    description: str
    credit: int # Credit of a debt account

class TransactionInfo(typing.NamedTuple):
    date: datetime.date
    description: str
    credit: int
    debt_account: Account
    credit_account: Account