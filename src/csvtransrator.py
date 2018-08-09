
import csv
from typing import List
from csvlineparser import Parser
from suicaparser import SuicaParser

class CsvTransrator():
    def __init__(self, parser_candidates: List[Parser]):
        self.parser_candidates = parser_candidates

    def csv2transaction_info(self, f):
        reader = csv.reader(f)

        self.parser = self.choose_parser(next(reader))

        # Skip headers and the first "unknown withdrawal" row
        for _ in range(self.parser.line_skip - 1):
            next(reader)
        return map(self.parser.extract_transaction_info, reader)
    
    def choose_parser(self, first_line) -> Parser:
        parsers = list(filter(lambda t: t.is_applicable(first_line), self.parser_candidates))
        if len(parsers) < 1:
            raise SystemError("Could not find matching parser for csv with the following line:\n    ", first_line)
        elif len(parsers) > 1:
            raise SystemError("Found more than one matching parser for csv with the following line:\n    ", first_line)
        return parsers[0]

class CsvTransactionsReader():

    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def __enter__(self):
        self.f = open(self.csv_path, 'r', newline='')
        t = CsvTransrator([SuicaParser()])

        return (t.csv2transaction_info(self.f), t.parser.receiving_account)

    def __exit__(self, type, value, traceback):
        self.f.close()