import piecash
from gnucash_csv_importer.account import Account

class PersonalBook:
    def generate_account_map(self, book: piecash.Book):
        raise NotImplementedError()

