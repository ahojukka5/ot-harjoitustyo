"""Fetching tools to collect energy price data.

This module contains functions to fetch data from internet sources to the
database.

Typical usage example:

  db = fetch("test")

As a result, a new database object is returned, containing data from source
"test".

Some sources might need configurations, for example, local data source needs
the name of the file and fetching from internet requires url from where to
fetch. Those options are given in `settings.py` and can be overridden with
environment variables.
"""

import json
import pandas as pd
import requests

from repositories import Database
from entities import Record

from tests import TEST_DATA_ENERGY_PRICE
import settings


def _to_record(row, price_row_name="PriceNoTax"):
    time = pd.to_datetime(row["DateTime"]).to_pydatetime()
    price = row[price_row_name]
    record = Record(time, price)
    return record


def _fetch_test(database):
    for row in TEST_DATA_ENERGY_PRICE:
        database.add_record(_to_record(row, price_row_name="Price"))
    return database


def _fetch_internet(database):
    for row in requests.get(settings.ENERGY_PRICE_URI, timeout=10).json():
        database.add_record(_to_record(row))
    return database


def _fetch_local(database):
    with open(settings.ENERGY_PRICE_FILE, encoding="utf8") as fid:
        for row in json.load(fid):
            database.add_record(_to_record(row))
    return database


def fetch_energy_price(source):
    """Fetch energy price data from internet or from a local source.

    Args:
        source (str): either "test" or "internet" or "local"

    Returns:
        Database: populated with data
    """
    if source not in ("test", "internet", "local"):
        raise NotImplementedError(f"Unknown source {source}")
    fetcher = {"test": _fetch_test, "internet": _fetch_internet, "local": _fetch_local}
    return fetcher[source](Database())
