# coding: utf-8
import piecash
import csv
import datetime 
import typing
import enum

class Account(enum.Enum):
    CARD = enum.auto()
    TRANSPORTATION = enum.auto()
    MEALS = enum.auto()
    SNACK = enum.auto()
    UNKNOWN = enum.auto()


class TransactionInfo(typing.NamedTuple):
    date: datetime.date
    description: str
    deposit: int
    account: Account
        
class CsvTransactionReader:
    """Works specifically with CSV generated from an android app'ICカードリーダー'."""
    
    @staticmethod
    def __extract_transaction_info(row):
        date = datetime.datetime.strptime(row[0], '%Y/%m/%d').date()
        desc = ', '.join(filter(lambda x: x != '', row[1:6]))
        deposit = - int(row[7]) if row[7] != '' else int(row[9])
        if deposit > 0:
            account = Account.CARD
        elif '自動改札機' in desc or 'バス等車載端末' in desc:
            account = Account.TRANSPORTATION
        else:
            if deposit  < -1000:
                account = Account.UNKNOWN
            elif deposit < -200:
                account = Account.MEALS
            else:
                account = Account.SNACK

        
        return TransactionInfo(date, desc, deposit, account)
        
    @staticmethod
    def csv2transaction_info(csv_path):
        with open(csv_path, 'r', newline='') as f:
            reader = csv.reader(f)

            # Skip headers and the first "unknown withdrawal" row
            for _ in range(6):
                next(reader)
                
            # At most 100 rows, so making a list is OK.
            # Otherwise, it will be closed before used.
            return list(map(CsvTransactionReader.__extract_transaction_info, reader))

def import_transactions(book_path, csv_path, dry=False, verborse=True):
    tr_candiates = CsvTransactionReader.csv2transaction_info(csv_path)
    with piecash.open_book(book_path, readonly=False) as book:
        accMap = {
            Account.CARD: book.accounts(name="JR related"),
            Account.TRANSPORTATION: book.accounts(name="Public Transportation"),
            Account.MEALS: book.accounts(name="Food").children(name="Meals"),
            Account.SNACK: book.accounts(name="Food").children(name="Snack"),
            Account.UNKNOWN: book.accounts(name="Imbalance-JPY")
            }
        suica = book.accounts(name="Suica")
        latest_date = suica.splits[-1].transaction.post_date
        transactions = []
        count = 1
        for info in tr_candiates:
            # Add only new transactions. Assumptions: new ones come with later dates
            if  latest_date < info.date:
                transactions.append(piecash.Transaction(currency=suica.commodity, description=info.description, post_date=info.date, num = str(count),
                                         splits=[
                    piecash.Split(account=suica, value=info.deposit),
                    piecash.Split(account=accMap[info.account], value=-info.deposit),
                ]))
                count +=1

        if verborse:
            book.flush()
            for transaction in transactions:
                print(piecash.ledger(transaction))
        if not dry:
            book.save()



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Import transactions to a gnucash book from a csv file.')
    parser.add_argument('book_path', type=str)
    parser.add_argument('csv_path', type=str)
    parser.add_argument('--dry', action='store_true')
    args = parser.parse_args()

    print("Imporing ", args.csv_path)
    import_transactions(args.book_path, args.csv_path, dry=args.dry)

