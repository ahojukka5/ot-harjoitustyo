"""Fetching tools to collect data.

This module contains functions to fetch data from internet sources to the
database.

Typical usage example:

  db = fetch("test")

As a result, a new database object is returned, containing data from source
"test".
"""

import pandas as pd
import requests

from database import Database
from record import Record

from tests import TEST_DATA


# internally used function, undocumented
def _to_record(row):
    time = pd.to_datetime(row["DateTime"]).to_pydatetime()
    price = row["PriceNoTax"]
    record = Record(time, price)
    return record


def fetch(source):
    """Fetch price data from internet source.

    Args:
        source (str): either "test" or "spot-hinta.fi"

    Returns:
        Database: populated with data
    """
    database = Database()
    if source == "test":
        for row in TEST_DATA:
            database.add_record(_to_record(row))
        return database
    if source == "spot-hinta.fi":
        url = "https://api.spot-hinta.fi/TodayAndDayForward"
        for row in requests.get(url, timeout=10).json():
            database.add_record(_to_record(row))
        return database

    raise NotImplementedError(f"data source {source} not implemented")
