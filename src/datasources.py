from database import Database
from record import Record

import pandas as pd
import requests

from tests import TEST_DATA


def to_record(row):
    time = pd.to_datetime(row["DateTime"]).to_pydatetime()
    price = row["PriceNoTax"]
    record = Record(time, price)
    return record


def fetch(source):
    database = Database()
    if source == "test":
        for row in TEST_DATA:
            database.add_record(to_record(row))
        return database
    elif source == "spot-hinta.fi":
        url = "https://api.spot-hinta.fi/TodayAndDayForward"
        for row in requests.get(url).json():
            database.add_record(to_record(row))
        return database

    raise NotImplementedError(f"data source {source} not implemented")
