
from nose.tools import ok_, eq_

import datetime
from gnucash_csv_importer.personal.suicaparser import SuicaParser
from gnucash_csv_importer.personal.myaccount import MyAccount
from gnucash_csv_importer.common import PartialTransactionInfo

class TestSuicaParser():

    def setUp(self):
        self.parser = SuicaParser()

    def test_is_applicable(self):
        ok_(self.parser.is_applicable("カードID,00000000000000"))

    def test_extract_fields_negative(self):
        row = ["2018/07/30", "自動販売機", "物品購入", "","","","","268","4881",""]
        eq_(self.parser.extract_fields(row),
            PartialTransactionInfo(
                datetime.datetime(2018, 7, 30, 0, 00).date(),
                "自動販売機, 物品購入",
                -268)
        )

    def test_extract_fields_positive(self):
        row = ["2018/07/30", "Charge", "", "","","","","","4881","3000"]
        eq_(self.parser.extract_fields(row),
            PartialTransactionInfo(
                datetime.datetime(2018, 7, 30, 0, 00).date(),
                "Charge",
                3000)
        )
    
    def test_choose_given_account_card(self):
        info =  PartialTransactionInfo(
                datetime.datetime(2018, 7, 30, 0, 00).date(),
                "Charge",
                3000)
        eq_(self.parser.choose_giving_account(info), MyAccount.CARD)
    
    def test_choose_given_account_trans(self):
        info =  PartialTransactionInfo(
            datetime.datetime(2018, 7, 30, 0, 00).date(),
            "自動改札機",
            -200)
        eq_(self.parser.choose_giving_account(info), MyAccount.TRANSPORTATION)
        
    def test_choose_given_account_unknown(self):
        info =  PartialTransactionInfo(
            datetime.datetime(2018, 7, 30, 0, 00).date(),
            "Dining",
            -2000)
        eq_(self.parser.choose_giving_account(info), MyAccount.UNKNOWN)

    def test_choose_given_account_meals(self):
        info =  PartialTransactionInfo(
        datetime.datetime(2018, 7, 30, 0, 00).date(),
        "Dining",
        -500)
        eq_(self.parser.choose_giving_account(info), MyAccount.MEALS)

    def test_choose_given_account_snack(self):
        info =  PartialTransactionInfo(
        datetime.datetime(2018, 7, 30, 0, 00).date(),
        "Dining",
        -100)
        eq_(self.parser.choose_giving_account(info), MyAccount.SNACK)
