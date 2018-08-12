import piecash
from gnucash_csv_importer.personal.myaccount import MyAccount as Account
from gnucash_csv_importer.personalbook import PersonalBook

class MyBook(PersonalBook):
    def generate_account_map(self, book: piecash.Book):
        m = {
                Account.CARD: book.accounts(name="JR related"),
                Account.TRANSPORTATION: book.accounts(name="Public Transportation"),
                Account.MEALS: book.accounts(name="Food").children(name="Meals"),
                Account.SNACK: book.accounts(name="Food").children(name="Snack"),
                Account.SUICA: book.accounts(name="Suica"),
                Account.SMBC_CARD_AMAZON: book.accounts(name="Amazon Mastercard Classic").children(name="Amazon Related"),
                Account.SMBC_CARD_OTHERS: book.accounts(name="Amazon Mastercard Classic").children(name="Others"),
                Account.UNKNOWN: book.accounts(name="Imbalance-JPY")
            }
        if len(set(m) ^ set(Account.__members__.values())) != 0:
            raise NotImplementedError("account association is not exaustive. contact dev.")
        return m