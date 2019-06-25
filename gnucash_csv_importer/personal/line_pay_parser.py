
import re
import datetime
from gnucash_csv_importer.parser import Parser
from gnucash_csv_importer.common import PartialTransactionInfo, TransactionInfo
from gnucash_csv_importer.personal.myaccount import MyAccount


class LinePayParser(Parser):
    def is_applicable(self, first_line):
        return 'LINEウォレットとのトーク履歴' in first_line
    
    def __call__(self, f):
        line = f.readline()
        repattern = re.compile(r"(\d{4}/\d{2}/\d{2})")
        transactions = []
        while line:
            is_date = repattern.match(line)
            if is_date:
                date = datetime.datetime.strptime(is_date.group(1), '%Y/%m/%d').date()
                time_line = f.readline()
                while ':' in time_line:
                    transaction = self.parse_post(f, date, time_line)
                    if transaction is not None:
                        transactions.append(transaction)
                    time_line = f.readline()
            line = f.readline()
        return transactions

    def parse_post(self, f, date, time_line):
        if '円' not in time_line:
            while ']' not in f.readline():
                pass
            return None 
        else:
            is_credit = re.search(r"チャージ (?P<amount>\d{1,3}(,\d{3})*) 円", time_line)
            is_debt = re.search(r"お支払い (?P<amount>\d{1,3}(,\d{3})*) 円", time_line)
            if is_credit:
                credit = int(is_credit.group('amount').replace(',', ''))
                f.readline()
                m = re.search(r": (?P<credit_acc_name>.+)", f.readline())
                name = m.group('credit_acc_name')
                if (name == 'ゆうちょ銀行') :
                    credit_account = MyAccount.JP_BANK
                    desc = 'Charge'
                else:
                    credit_account = MyAccount.UNKNOWN
                    desc = name
            elif is_debt:
                credit = - int(is_debt.group('amount').replace(',', ''))
                credit_account = MyAccount.UNKNOWN
                f.readline()
                m = re.search(r": (?P<credit_acc_name>.+)", f.readline())
                desc = m.group('credit_acc_name')
            else:
                raise ValueError(f'illegal line\nNeither credit or debt.')
            
            while ']' not in f.readline():
                pass
            return TransactionInfo(date, desc, credit = credit, debt_account=MyAccount.LINE_PAY, credit_account=credit_account)
