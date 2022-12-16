"""Utility functions and helpers to be used internally.
"""


def get_cheapest_hour(database):
    """Return the cheapest hour from the database.

    Args:
        database: a non-empty Database object.

    Returns:
        A Record where energy price is cheapest.
    """
    cheapest_record = None
    cheapest_price = 2**32
    records = database.get_records()
    assert len(records) > 0
    for record in records:
        if record.get_price() < cheapest_price:
            cheapest_record = record
            cheapest_price = record.get_price()
    return cheapest_record
