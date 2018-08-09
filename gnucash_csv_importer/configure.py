from gnucash_csv_importer.parser.suicaparser import SuicaParser
from gnucash_csv_importer.csvtransrator import CsvTransactionsReader, CsvTransrator
from gnucash_csv_importer.import2book import Import2Book
from gnucash_csv_importer.mybook import MyBook

#DI like
import2book = Import2Book(
    CsvTransactionsReader(
        CsvTransrator(
            [
                SuicaParser()
                ]
            )),
    MyBook()
    )
