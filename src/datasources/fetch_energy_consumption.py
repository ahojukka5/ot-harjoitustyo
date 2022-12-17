"""Fetching tools to collect energy consumption data.

Typical usage example:

  db = fetch("test")

As a result, a new database object is returned, containing data from source
"test".
"""

import pandas as pd
import settings
from repositories import Database
from entities import Record
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


def _fetch_local(database, consumption_file=settings.ENERGY_CONSUMPTION_FILE):
    data = pd.read_csv(
        consumption_file,
        delimiter=";",
        decimal=",",
        index_col=4,
        parse_dates=True,
    ).tz_convert("Europe/Helsinki")
    for idx, row in data.tail(3 * 24).iterrows():
        time = pd.to_datetime(str(idx)).to_pydatetime()
        amount = row["Määrä"]
        record = Record(time, amount)
        database.add_record(record)
    return database


def fetch_energy_consumption(source):
    """Fetch energy consumption data from internet or from a local source.

    Args:
        source (str): either "test" or "local"

    Returns:
        Database: populated with data
    """
    if source not in ("test", "local"):
        raise NotImplementedError(f"Unknown source {source}")
    fetcher = {"test": _fetch_test, "local": _fetch_local}
    return fetcher[source](Database())
