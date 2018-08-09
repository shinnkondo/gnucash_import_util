import datetime

from typing import List
from gnucash_csv_importer.common import PartialTransactionInfo, TransactionInfo
from gnucash_csv_importer.account import Account
from gnucash_csv_importer.csvlineparser import Parser


class SuicaParser(Parser):
    """Works specifically with CSV generated from an android app'ICカードリーダー'."""
    line_skip: int = 6
    receiving_account = Account.SUICA

    def is_applicable(self, first_line):
        return 'カードID' in first_line

    def extract_fields(self, row: List[str]):
        date = datetime.datetime.strptime(row[0], '%Y/%m/%d').date()
        desc = ', '.join(filter(lambda x: x != '', row[1:6]))
        deposit = - int(row[7]) if row[7] != '' else int(row[9])
        return PartialTransactionInfo(date, desc, deposit)

    def choose_giving_account(self, info: PartialTransactionInfo):
        if info.deposit > 0:
            return Account.CARD
        elif any(keyword in info.description for keyword in ('自動改札機', 'バス等車載端末')):
            return Account.TRANSPORTATION
        else:
            if info.deposit  < -1000:
                return Account.UNKNOWN
            elif info.deposit < -200:
                return Account.MEALS
            else:
                return Account.SNACK