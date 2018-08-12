from typing import List, Dict
from piecash import Split
import datetime
import warnings

class Reconciler:

    def __init__(self, split_candidates: List[Split]):
        self.split_candidates: Dict[datetime.date, Split] = {} 
        for split in split_candidates:
            if split.reconcile_state == "y":
                continue

            if not split.transaction.post_date in self.split_candidates:
                self.split_candidates[split.transaction.post_date] = {split.value: [split]}
                continue

            value2split = self.split_candidates[split.transaction.post_date]

            if not split.value in value2split:
                value2split[split.value] = [split]
                continue

            warnings.warn("There exists unreconciled split with the same date and the value in ", split.transaction.description, ". Reconciliation may be inaccurate.")
            value2split[split.value].append(split) 
                
            

    def reconcile(self, date, price):
        """Try to reconcile the splits and return the result. If success, mark the split.
        Reconciliation succeed if there is a split with the same date and the same price.
        """
        
        if date in self.split_candidates and price in self.split_candidates[date]:
            # Only mark the last one as reconciled.
            self.split_candidates[date][price][-1].reconcile_state = "c"
            return True
        else:
            return False