import datetime

from typing import List
from gnucash_csv_importer.common import PartialTransactionInfo, TransactionInfo
from gnucash_csv_importer.personal.myaccount import MyAccount as Account
from gnucash_csv_importer.parser import CSVParser


class SuicaParser(CSVParser):
    """Works specifically with CSV generated from an android app'ICカードリーダー'."""
    line_skip: int = 6
    debt_account = Account.SUICA

    def is_applicable(self, first_line):
        return 'カードID' in first_line

    def extract_fields(self, row: List[str]):
        date = datetime.datetime.strptime(row[0], '%Y/%m/%d').date()
        desc = ', '.join(filter(lambda x: x != '', row[1:6]))
        credit = - int(row[7]) if row[7] != '' else int(row[9])
        return PartialTransactionInfo(date, desc, credit)

    def choose_credit_account(self, info: PartialTransactionInfo):
        if info.credit > 0:
            return Account.CARD
        elif any(keyword in info.description for keyword in ('自動改札機', 'バス等車載端末')):
            return Account.TRANSPORTATION
        else:
            if info.credit  < -1000:
                return Account.UNKNOWN
            elif info.credit < -200:
                return Account.MEALS
            else:
                return Account.SNACK