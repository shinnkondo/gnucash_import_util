from typing import List
import re
import datetime

from gnucash_csv_importer.common import PartialTransactionInfo, TransactionInfo
from gnucash_csv_importer.parser import CSVParser
from gnucash_csv_importer.personal.myaccount import MyAccount


class SmbcCardParser(CSVParser):
    line_skip: int = 0

    def is_applicable(self, first_line) -> bool:
        return re.match(r"\d+/\d+/\d+.*", first_line)

    def extract_fields(self, row: List[str]) -> PartialTransactionInfo:
        date = datetime.datetime.strptime(row[0], '%Y/%m/%d').date()
        desc = row[1]
        credit = - int(row[6])
        return PartialTransactionInfo(date, desc, credit)

    def choose_credit_account(self, info: PartialTransactionInfo):
        return MyAccount.UNKNOWN

    def choose_debt_account(self, info: PartialTransactionInfo):
        if re.match(r"amazon|ａｍａｚｏｎ", info.description, flags=re.IGNORECASE):
            return MyAccount.SMBC_CARD_AMAZON
        else:
            return MyAccount.SMBC_CARD_OTHERS

    def extract_transaction_info(self, row):
        """The interface method to be used"""
        p = self.extract_fields(row)
        return TransactionInfo(p.date, p.description, p.credit, debt_account=self.choose_debt_account(p), credit_account=self.choose_credit_account(p))
