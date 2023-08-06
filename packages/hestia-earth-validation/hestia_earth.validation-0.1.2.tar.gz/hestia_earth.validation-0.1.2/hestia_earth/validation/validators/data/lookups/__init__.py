import os
import sys
import csv
import numpy as np

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.append(CURRENT_DIR)
DELIMITER = '\t'
ENCODING = 'ISO-8859-1'


def recfromcsv_mod(filename: str, **kwargs):
    def rewrite_csv_as_tab():
        with open(filename, 'r', encoding=ENCODING) as fp:
            reader = csv.reader(fp)
            for row in reader:
                yield DELIMITER.join(row)
    return np.recfromcsv(rewrite_csv_as_tab(), delimiter=DELIMITER, **kwargs)


def import_lookup_table(filename: str):
    """Method that imports a lookup table necessary to carry out the calculation.
        Arguments:
            filename: The name of the file.
        Returns a pandas.DataFrame object."""
    return recfromcsv_mod(os.path.join(CURRENT_DIR, filename), encoding=ENCODING)


def column_name(key: str): return key.replace(',', '').replace(' ', '_').lower()


def get_table_value(df, col_match, col_match_with, col_val): return df[df[col_match] == col_match_with][col_val]
