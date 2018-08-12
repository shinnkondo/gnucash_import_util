from datetime import datetime
from piecash import Split, Transaction

from unittest.mock import MagicMock
from nose.tools import ok_, eq_

from gnucash_csv_importer.reconciler import Reconciler

class TestReconciler:

    def setUp(self):
        self.date = datetime(2018, 7, 30, 0, 00).date()
        self.price = 1000
        splits = [
            Split(account=None,
            value=self.price,
            transaction=Transaction(currency=None, post_date=self.date),
            reconcile_state='n'
            )
        ]
        self.reconciler = Reconciler(splits)

    def test_reconcile(self):
        ok_(self.reconciler.reconcile(self.date, 1000))
        eq_(self.reconciler.split_candidates[self.date][self.price][-1].reconcile_state, 'c')
    
    def test_reconcile_different_value(self):
        ok_(not self.reconciler.reconcile(self.date, 777))
        eq_(self.reconciler.split_candidates[self.date][self.price][-1].reconcile_state, 'n')

    def test_reconcile_different_date(self):
        ok_(not self.reconciler.reconcile(datetime(2018, 6, 15, 0, 00).date(), 777))
        eq_(self.reconciler.split_candidates[self.date][self.price][-1].reconcile_state, 'n')
