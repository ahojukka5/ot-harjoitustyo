class Record:
    def __init__(self, time, energy_price):
        self.time = time
        self.energy_price = energy_price

    def get_time(self):
        return self.time

    def get_energy_price(self):
        return self.energy_price

    def to_dict(self):
        return {"time": self.get_time(), "energy_price": self.get_energy_price()}
