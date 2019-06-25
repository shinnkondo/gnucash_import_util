import datetime

from nose.tools import eq_, ok_
from unittest.mock import MagicMock
from gnucash_csv_importer.common import PartialTransactionInfo, TransactionInfo
from gnucash_csv_importer.personal.myaccount import MyAccount
from gnucash_csv_importer.personal.line_pay_parser import LinePayParser


class TestLinePayParser:

    def setUp(self):
        self.parser = LinePayParser()
        self.date = datetime.datetime(2018, 8, 8, 0, 00).date()

    def test_is_applicable(self):
        line = "[LINE] LINEウォレットとのトーク履歴"
        ok_(self.parser.is_applicable(line))
    
    def test_is_applicable_not(self):
        line = "Company,ご本人,1回払い,,'18/09,740,740,,,,,"
        ok_(not self.parser.is_applicable(line))

    def test_is_row_valid_blank(self):
        row = [""]
        ok_(not self.parser.is_row_vaild(row))

    def test_is_row_valid_date_not_valid_but_set_date(self):
        row = ["2018/08/08(火)"]
        ok_(not self.parser.is_row_vaild(row))
        eq_(self.parser.date, self.date)
    
    def test_is_row_valid_not_ok(self):
        row = ["15:03","LINEウォレット", "[LINE Pay ZaimはLINE Pay利用履歴の提供をリクエストしています。Zaimと連動するには、同意画面に移動して情報の提供に同意してください。]"]
        ok_(not self.parser.is_row_vaild(row))
    def test_is_row_valid_ok(self):
        row = ["15:03","LINEウォレット", "[LINE Pay お支払い 198 円お支払いが完了しました。加盟店: 株式会社ローソン付与予定ポイント: 5 P決済後の残高: 10,109 円]"]
        ok_(self.parser.is_row_vaild(row))

    def test_extract_transaction_info_debt(self):
        self.parser.date = self.date
        row = ["15:03","LINEウォレット", "[LINE Pay お支払い 198 円お支払いが完了しました。加盟店: 株式会社ローソン付与予定ポイント: 5 P決済後の残高: 10,109 円]"]
        eq_(self.parser.extract_transaction_info(row),
            TransactionInfo(self.date,
            description="株式会社ローソン",
            credit=-198,
            debt_account=MyAccount.LINE_PAY,
            credit_account=MyAccount.UNKNOWN)
        )

    def test_extract_transaction_info_credit(self):
        self.parser.date = self.date
        row = ["15:03","LINEウォレット", "[LINE Pay チャージ 1,000 円チャージしました。銀行名: ゆうちょ銀行LINE Pay株式会社 / 資金移動業者 関東財務局長第00036号]"]
        eq_(self.parser.extract_transaction_info(row),
            TransactionInfo(self.date,
            description="Charge",
            credit=1000,
            debt_account=MyAccount.LINE_PAY,
            credit_account=MyAccount.JP_BANK)
        )
