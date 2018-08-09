from typing import List

from common import PartialTransactionInfo, TransactionInfo
from account import Account

class Parser:
    line_skip: int
    receiving_account: Account

    def is_applicable(self, first_line) -> bool:
        raise NotImplementedError

    def extract_fields(self, row: List[str]) -> PartialTransactionInfo:
        raise NotImplementedError

    def choose_giving_account(self, info: PartialTransactionInfo) -> Account:
        return Account.UNKNOWN

    def extract_transaction_info(self, row):
        """The interface method to be used"""
        p = self.extract_fields(row)
        return TransactionInfo(p.date, p.description, p.deposit, self.choose_giving_account(p))