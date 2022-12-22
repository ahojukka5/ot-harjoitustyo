from entities import Selection

import dateutil.parser
import datetime


class DateTimePicker:
    def __init__(self):
        self._selection = Selection()

    def clear(self):
        self._selection = Selection()

    def pick(self, start):
        if isinstance(start, str):
            start = dateutil.parser.parse(start)
        end = start + datetime.timedelta(hours=1)
        self._selection.add_timerange(start, end)
        return self

    def pick_between(self, start, end):
        if isinstance(start, str):
            start = dateutil.parser.parse(start)
        if isinstance(end, str):
            end = dateutil.parser.parse(end)
        self._selection.add_timerange(start, end)
        return self

    def to_selection(self):
        return self._selection
