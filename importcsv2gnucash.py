import argparse
from gnucash_csv_importer.configure import configure
from gnucash_csv_importer.personal.mybook import MyBook
from gnucash_csv_importer.personal.suicaparser import SuicaParser

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Import transactions to a gnucash book from a csv file.')
    parser.add_argument('book_path', type=str)
    parser.add_argument('csv_path', type=str)
    parser.add_argument('--dry', action='store_true')
    args = parser.parse_args()

    print("Imporing ", args.csv_path)
    configure([SuicaParser()], MyBook()).import_transactions(args.book_path, args.csv_path, dry=args.dry)