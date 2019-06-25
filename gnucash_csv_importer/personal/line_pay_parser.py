
import re
import datetime
from gnucash_csv_importer.parser import Parser
from gnucash_csv_importer.common import PartialTransactionInfo, TransactionInfo
from gnucash_csv_importer.personal.myaccount import MyAccount


class LinePayParser(Parser):
    line_skip: int = 2
    delimiter: str = '\t'

    def is_applicable(self, first_line):
        return 'LINEウォレットとのトーク履歴' in first_line

    def extract_transaction_info(self, row):
        is_credit = re.search(r"チャージ (?P<amount>\d{1,3}(,\d{3})*) 円チャージ[^:]+: (?P<credit_acc_name>.+)LINE Pay株式会社", row[2])
        is_debt = re.search(r"お支払い (?P<amount>\d{1,3}(,\d{3})*) 円お支払いが完了しました。加盟店: (?P<credit_acc_name>.+)付与予定", row[2])
        
        if is_credit:
            credit = int(is_credit.group('amount').replace(',', ''))
            name = is_credit.group('credit_acc_name')
            credit_account = MyAccount.JP_BANK if (name == 'ゆうちょ銀行') else MyAccount.UNKNOWN
            desc = 'Charge'

        elif is_debt:
            credit = - int(is_debt.group('amount').replace(',', ''))
            credit_account = MyAccount.UNKNOWN
            desc = is_debt.group('credit_acc_name')
        else:
            raise ValueError(f'illegal line {row}\nNeither credit or debt.')

        return TransactionInfo(self.date, desc, credit = credit, debt_account=MyAccount.LINE_PAY, credit_account=credit_account)
    
    def is_row_vaild(self, row):
        
        if len(row) == 0:
            return False
        else:
            is_date = re.match(r"(\d{4}/\d{2}/\d{2})", row[0])
            if is_date:
                self.date = datetime.datetime.strptime(is_date.group(1), '%Y/%m/%d').date()
                return False
            elif re.match(r"\d{1,2}:\d{2}", row[0]) and '円' in row[2]:
                return True
        return False
