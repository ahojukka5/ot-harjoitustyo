import unittest
from datasources import fetch

import pandas as pd


class TestRecord(unittest.TestCase):
    def test_fetch_test_data(self):
        data = fetch("test").to_dataframe()
        first_row = data.iloc[0]
        print(first_row)
        self.assertEqual(0.1563, first_row["energy_price"])
        print(first_row.index)
        print(first_row.name)
        self.assertEqual(pd.Timestamp("2022-11-28T00:00:00+02:00"), first_row.name)
