from entities import Selection


class DateTimePicker:
    def __init__(self):
        self._selections = []

    def pick(self, start):
        self._selections.append(Selection(start))

    def get_selections(self):
        return self._selections
