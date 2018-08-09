# coding: utf-8
import piecash

from gnucash_csv_importer.csvtransrator import CsvTransactionsReader
from gnucash_csv_importer.account import Account

def import_transactions(book_path, csv_path, dry=False, verborse=True):
    with piecash.open_book(book_path, readonly=False) as book:
        accMap = generate_account_map(book)
        with CsvTransactionsReader(csv_path) as (tr_candidates, receiving_account):
            transactions = execute_transactions(receiving_account, accMap, tr_candidates)
        if verborse:
            book.flush()
            for transaction in transactions:
                print(piecash.ledger(transaction))
        if not dry:
            book.save()

def execute_transactions(receiving_account: Account, accountMap, transaction_candidates):
    latest_date = accountMap[receiving_account].splits[-1].transaction.post_date
    transactions = []
    count = 1
    for info in transaction_candidates:
        # Add only new transactions. Assumptions: new ones come with later dates
        if  latest_date >= info.date:
            continue

        transaction = piecash.Transaction(currency=accountMap[receiving_account].commodity, description=info.description, 
            post_date=info.date, num = str(count),
            splits=[
                piecash.Split(account=accountMap[receiving_account], value=info.deposit),
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



