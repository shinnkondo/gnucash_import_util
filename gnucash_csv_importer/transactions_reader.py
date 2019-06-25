import csv
from typing import List
from gnucash_csv_importer.parser import CSVParser

class Transrator:
    def __init__(self, parser_candidates: List[CSVParser]):
        self.parser_candidates = parser_candidates

    def get_transaction_info(self, f):
        p = f.tell()
        self.parser = self.choose_parser(f.readline())
        f.seek(p)
        if isinstance(self.parser, CSVParser):
            return self.csv2transaction_info(f)
        else:
            return self.parser(f)

    def csv2transaction_info(self, f):
        reader = csv.reader(f)

        # Skip headers and the first "unknown withdrawal" row
        for _ in range(self.parser.line_skip):
            next(reader)
        return map(self.parser.extract_transaction_info, [row for row in reader if self.parser.is_row_vaild(row)])
    
    def choose_parser(self, first_line) -> CSVParser:
        parsers = list(filter(lambda t: t.is_applicable(first_line), self.parser_candidates))
        if len(parsers) < 1:
            raise SystemError("Could not find matching parser for csv with the following line:\n    ", first_line)
        elif len(parsers) > 1:
            raise SystemError("Found more than one matching parser for csv with the following line:\n    ", first_line)
        return parsers[0]


class TransactionsReader:

    def __init__(self, translator: Transrator):
        self.translator = translator
        
    def open(self, csv_path: str):
        self.csv_path = csv_path
        return self

    def __enter__(self):
        self.f = open(self.csv_path, 'r', newline='')
        t = self.translator

        return t.get_transaction_info(self.f)

    def __exit__(self, type, value, traceback):
        self.f.close()