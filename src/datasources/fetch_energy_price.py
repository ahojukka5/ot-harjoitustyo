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

import pandas as pd
import requests
import json

from database import Database
from record import Record

from tests import TEST_DATA
import settings


def _to_record(row):
    time = pd.to_datetime(row["DateTime"]).to_pydatetime()
    price = row["PriceNoTax"]
    record = Record(time, price)
    return record


def _fetch_test(database):
    for row in TEST_DATA:
        database.add_record(_to_record(row))
    return database


def _fetch_internet(database):
    for row in requests.get(settings.ENERGY_PRICE_URI, timeout=10).json():
        database.add_record(_to_record(row))
    return database


def _fetch_local(database):
    for row in json.load(open(settings.ENERGY_PRICE_FILE)):
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
