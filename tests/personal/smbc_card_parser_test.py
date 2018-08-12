import datetime

from nose.tools import eq_, ok_
from unittest.mock import MagicMock

from gnucash_csv_importer.common import PartialTransactionInfo, TransactionInfo
from gnucash_csv_importer.personal.myaccount import MyAccount
from gnucash_csv_importer.personal.smbc_card_parser import SmbcCardParser


class TestSmbcCardParser:

    def setUp(self):
        self.parser = SmbcCardParser()
        self.date = datetime.datetime(2018, 8, 8, 0, 00).date()

    def test_is_applicable(self):
        line = "2018/8/8,Company,ご本人,1回払い,,'18/09,740,740,,,,,"
        ok_(self.parser.is_applicable(line))
    
    def test_is_applicable_not(self):
        line = "Company,ご本人,1回払い,,'18/09,740,740,,,,,"
        ok_(not self.parser.is_applicable(line))

    def test_choose_credit_account(self):
        row = ["what", "so", "ever", "1220"]
        eq_(self.parser.choose_credit_account(row), MyAccount.UNKNOWN)
    
    def test_extract_fields(self):
        row = ['2018/8/8','Company', 'ご本人', '1回払い', '', "'18/09", '740', '740', '', '', '', '', '']
        eq_(self.parser.extract_fields(row),
        PartialTransactionInfo(
            date= self.date,
            description="Company",
            credit=-740
        ))

    def test_choose_debt_account_amazon(self):
        info = PartialTransactionInfo(
            date= self.date,
            description="ＡＭＡＺＯＮ．ＣＯ．ＪＰ",
            credit=-740
        )

        eq_(self.parser.choose_debt_account(info), MyAccount.SMBC_CARD_AMAZON)

    def test_choose_debt_account_others(self):
        info = PartialTransactionInfo(
            date=self.date,
            description="steam",
            credit=-740
        )

        eq_(self.parser.choose_debt_account(info), MyAccount.SMBC_CARD_OTHERS)

    def test_extract_transaction_info(self):
        row = ['2018/8/8','Company', 'ご本人', '1回払い', '', "'18/09", '740', '740', '', '', '', '', '']
        self.parser.extract_fields = MagicMock(return_value= PartialTransactionInfo(
            date=self.date,
            description="ＡＭＡＺＯＮ．ＣＯ．ＪＰ",
            credit=-740
        ))
        self.parser.choose_debt_account = MagicMock(return_value=MyAccount.SMBC_CARD_AMAZON)
        self.parser.choose_credit_account = MagicMock(return_value=MyAccount.UNKNOWN)

        eq_(self.parser.extract_transaction_info(row),
            TransactionInfo(self.date,
            description="ＡＭＡＺＯＮ．ＣＯ．ＪＰ",
            credit=-740,
            debt_account=MyAccount.SMBC_CARD_AMAZON,
            credit_account=MyAccount.UNKNOWN)
        )