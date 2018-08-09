import piecash
from gnucash_csv_importer.account import Account

class PersonalBook:
    def generate_account_map(self, book: piecash.Book):
        raise NotImplementedError()

class MyBook(PersonalBook):
    def generate_account_map(self, book: piecash.Book):
        return {
                Account.CARD: book.accounts(name="JR related"),
                Account.TRANSPORTATION: book.accounts(name="Public Transportation"),
                Account.MEALS: book.accounts(name="Food").children(name="Meals"),
                Account.SNACK: book.accounts(name="Food").children(name="Snack"),
                Account.SUICA: book.accounts(name="Suica"),
                Account.UNKNOWN: book.accounts(name="Imbalance-JPY")
            }