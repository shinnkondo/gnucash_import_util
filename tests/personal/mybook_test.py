from nose.tools import raises, ok_
from unittest.mock import MagicMock

from gnucash_csv_importer.personal.mybook import MyBook

class TestMyBook:
    def setUp(self):
        self.mybook = MyBook()

    ## Here to check impelemntation error checking
    # @raises(NotImplementedError)
    # def test_non_exaustive_generation_should_fail(self):
    #     book_mock = MagicMock()
    #     self.mybook.generate_account_map(book_mock)

    def test_non_exaustive_generation_should_not_fail(self):
        book_mock = MagicMock()
        self.mybook.generate_account_map(book_mock)
        ok_(True)