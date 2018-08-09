# coding: utf-8
import piecash
import csv
import datetime 
import typing
from typing import List
import enum

class Account(enum.Enum):
    CARD = enum.auto()
    TRANSPORTATION = enum.auto()
    MEALS = enum.auto()
    SNACK = enum.auto()
    SUICA = enum.auto()
    UNKNOWN = enum.auto()

class PartialTransactionInfo(typing.NamedTuple):
    date: datetime.date
    description: str
    deposit: int

class TransactionInfo(typing.NamedTuple):
    date: datetime.date
    description: str
    deposit: int
    account: Account

    @staticmethod
    def from_partial_transaction_info(info: PartialTransactionInfo, account: Account):
        return TransactionInfo(date=info.date, description=info.description, deposit=info.deposit, account=account)

class Parser():
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
    
class CsvTransrator():
    def __init__(self, parser_candidates: List[Parser]):
        self.parser_candidates = parser_candidates

    def csv2transaction_info(self, f):
        reader = csv.reader(f)

        parser = self.choose_parser(next(reader))

        # Skip headers and the first "unknown withdrawal" row
        for _ in range(parser.line_skip - 1):
            next(reader)
        return map(parser.extract_transaction_info, reader)
    
    def choose_parser(self, first_line) -> Parser:
        parsers = list(filter(lambda t: t.is_applicable(first_line), self.parser_candidates))
        if len(parsers) < 1:
            raise SystemError("Could not find matching parser for csv with the following line:\n    ", first_line)
        elif len(parsers) > 1:
            raise SystemError("Found more than one matching parser for csv with the following line:\n    ", first_line)
        return parsers[0]

class CsvTransactionsReader():

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def __enter__(self):
        self.f = open(self.csv_path, 'r', newline='')
        return CsvTransrator([SuicaParser()]).csv2transaction_info(self.f)

    def __exit__(self, type, value, traceback):
        self.f.close()

def import_transactions(book_path, csv_path, dry=False, verborse=True):
    with piecash.open_book(book_path, readonly=False) as book:
        accMap = generate_account_map(book)
        with CsvTransactionsReader(csv_path) as tr_candidates:
            transactions = execute_transactions(accMap[Account.SUICA], accMap, tr_candidates)
        if verborse:
            book.flush()
            for transaction in transactions:
                print(piecash.ledger(transaction))
        if not dry:
            book.save()

def execute_transactions(receiving_account, accountMap, transaction_candidates):
    latest_date = receiving_account.splits[-1].transaction.post_date
    transactions = []
    count = 1
    for info in transaction_candidates:
        # Add only new transactions. Assumptions: new ones come with later dates
        if  latest_date >= info.date:
            continue

        transaction = piecash.Transaction(currency=receiving_account.commodity, description=info.description, 
            post_date=info.date, num = str(count),
            splits=[
                piecash.Split(account=receiving_account, value=info.deposit),
                piecash.Split(account=accountMap[info.account], value=-info.deposit),
            ])
        transactions.append(transaction)
        count +=1
    return transactions

def generate_account_map(book):
    return {
            Account.CARD: book.accounts(name="JR related"),
            Account.TRANSPORTATION: book.accounts(name="Public Transportation"),
            Account.MEALS: book.accounts(name="Food").children(name="Meals"),
            Account.SNACK: book.accounts(name="Food").children(name="Snack"),
            Account.SUICA: book.accounts(name="Suica"),
            Account.UNKNOWN: book.accounts(name="Imbalance-JPY")
        }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Import transactions to a gnucash book from a csv file.')
    parser.add_argument('book_path', type=str)
    parser.add_argument('csv_path', type=str)
    parser.add_argument('--dry', action='store_true')
    args = parser.parse_args()

    print("Imporing ", args.csv_path)
    import_transactions(args.book_path, args.csv_path, dry=args.dry)

