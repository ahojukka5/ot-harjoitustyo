from database import Database
from record import Record

import pandas as pd

from tests import TEST_DATA


def fetch(source):
    database = Database()
    if source == "test":
        for row in TEST_DATA:
            time = pd.to_datetime(row["DateTime"]).to_pydatetime()
            price = row["PriceNoTax"]
            record = Record(time, price)
            database.add_record(record)
        return database
    raise NotImplementedError(f"data source {source} not implemented")
