from typing import List

from gnucash_csv_importer.common import PartialTransactionInfo, TransactionInfo
from gnucash_csv_importer.account import Account

class Parser:
    line_skip: int
    delimiter: str = ','
    debt_account: Account

    def is_applicable(self, first_line) -> bool:
        raise NotImplementedError

    def extract_fields(self, row: List[str]) -> PartialTransactionInfo:
        raise NotImplementedError

    def choose_credit_account(self, info: PartialTransactionInfo) -> Account:
        return NotImplementedError

    def extract_transaction_info(self, row):
        """The interface method to be used"""
        p = self.extract_fields(row)
        return TransactionInfo(p.date, p.description, p.credit, debt_account=self.debt_account, credit_account=self.choose_credit_account(p))

    def is_row_vaild(self, row) -> bool:
        return True
