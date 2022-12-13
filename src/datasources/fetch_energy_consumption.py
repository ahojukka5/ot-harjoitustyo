"""Fetching tools to collect energy consumption data.

Typical usage example:

  db = fetch("test")

As a result, a new database object is returned, containing data from source
"test".
"""

import pandas as pd
from database import Database
from record import Record
from tests import TEST_DATA_ENERGY_CONSUMPTION


def _to_record(row):
    time = pd.to_datetime(row["DateTime"]).to_pydatetime()
    amount = row["Amount"]
    record = Record(time, amount)
    return record


def _fetch_test(database):
    for row in TEST_DATA_ENERGY_CONSUMPTION:
        database.add_record(_to_record(row))
    return database


def fetch_energy_consumption(source):
    """Fetch energy consumption data from internet or from a local source.

    Args:
        source (str): either "test" or "internet" or "local"

    Returns:
        Database: populated with data
    """
    if source not in ("test", "internet", "local"):
        raise NotImplementedError(f"Unknown source {source}")
    fetcher = {"test": _fetch_test}
    return fetcher[source](Database())
