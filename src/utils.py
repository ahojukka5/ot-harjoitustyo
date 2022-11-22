def get_cheapest_hour(database):
    cheapest_record = None
    cheapest_price = 2**32
    records = database.get_records()
    assert len(records) > 0
    for record in records:
        if record.get_energy_price() < cheapest_price:
            cheapest_record = record
            cheapest_price = record.get_energy_price()
    return cheapest_record
