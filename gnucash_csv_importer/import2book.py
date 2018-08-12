# coding: utf-8
import datetime
from typing import Dict, Iterator

import piecash

from gnucash_csv_importer.account import Account
from gnucash_csv_importer.common import TransactionInfo
from gnucash_csv_importer.csvtransrator import CsvTransactionsReader
from gnucash_csv_importer.personalbook import PersonalBook
from gnucash_csv_importer.reconciler import Reconciler

# DI like

class Import2Book:

    def __init__(self, csvTransactionsReader: CsvTransactionsReader, personalbook: PersonalBook):
        self.csvTransactionsReader = csvTransactionsReader
        self.persobalbook = personalbook

    def import_transactions(self, book_path, csv_path, dry=False, verborse=True):
        with piecash.open_book(book_path, readonly=dry) as book:
            accMap = self.persobalbook.generate_account_map(book)
            with self.csvTransactionsReader.open(csv_path) as tr_candidates:
                transactions = self.execute_transactions(accMap, tr_candidates)
            if verborse:
                book.flush()
                for transaction in transactions:
                    print(piecash.ledger(transaction))
            if not dry:
                book.save()

    def execute_transactions(self, accountMap, transaction_candidates: Iterator[TransactionInfo]):
        transactions = []
        count = 1

        reconcilers = {}

        for info in transaction_candidates:
            debt_account: piecash.Account = accountMap[info.debt_account]

            if not info.debt_account in reconcilers:
                reconcilers[info.debt_account] = Reconciler(debt_account.splits)
            if reconcilers[info.debt_account].reconcile(info.date, info.credit):
                continue

            transaction = piecash.Transaction(currency=debt_account.commodity, description=info.description, 
                post_date=info.date, num = str(count),
                splits=[
                    piecash.Split(account=debt_account, value=info.credit),
                    piecash.Split(account=accountMap[info.credit_account], value=-info.credit),
                ])
            transactions.append(transaction)
            count +=1
        return transactions
