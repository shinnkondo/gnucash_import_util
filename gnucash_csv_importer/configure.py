
from gnucash_csv_importer.csvtransrator import CsvTransactionsReader, CsvTransrator
from gnucash_csv_importer.import2book import Import2Book
from typing import List

from gnucash_csv_importer.personalbook import PersonalBook
from gnucash_csv_importer.parser import Parser

#DI like

def configure(parsers: List[Parser], personalbook: PersonalBook):
    return Import2Book(
    csvTransactionsReader=CsvTransactionsReader(
        CsvTransrator(
            parsers
            )),
    personalbook=personalbook
    )


