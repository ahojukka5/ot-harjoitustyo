import datetime
import os
import config


class IO:
    @staticmethod
    def print(*args, **kwargs):
        print(*args, **kwargs)

    @staticmethod
    def input(*args, **kwargs):
        return input(*args, **kwargs)


class TUI:
    """A simple Text User Interface"""

    def __init__(self, dataservice, datetimepicker, messageservice, _io=IO):
        self._dataservice = dataservice
        self._datetimepicker = datetimepicker
        self._messageservice = messageservice
        self._io = _io
        self._commands = {
            "V": self.pick,
            "C": self.clear,
            "G": self.calendar,
            "S": self.shelly,
            "Q": self.quit,
        }
        self._done = False

    def get_messageservice(self):
        return self._messageservice

    def get_dataservice(self):
        return self._dataservice

    def get_datetimepicker(self):
        return self._datetimepicker

    def get_io(self):
        return self._io

    @staticmethod
    def format_list_price(record, format_date=True):
        start = record.get_time().astimezone()
        end = start + datetime.timedelta(hours=1)
        hour = start.strftime("%H")
        next_hour = end.strftime("%H")
        date = start.strftime("%Y-%m-%d") if format_date else " " * 10
        price = record.get_price() * 100
        return f"{date} {hour} - {next_hour} : {price:5.2f}"

    def list_prices(self):
        out = self.get_io().print
        out(
            "\n"
            "Pörssisähkön tulevat hinnat:\n"
            "\n"
            "   ⭐   seuraavan kolmen halvimman tunnin joukossa\n"
            "   ✅   valittu tunti\n"
            "\n"
        )
        dataservice = self.get_dataservice()
        picker = self.get_datetimepicker()
        cheap_hours = dataservice.find_cheapest_hours(hours=3)
        selected_hours = picker.to_selection()
        for (rownum, record) in enumerate(dataservice.get_future_prices()):
            start_time = record.get_time().astimezone()
            format_date = rownum == 0 or start_time.hour == 0
            line = self.format_list_price(record, format_date=format_date)
            line += " ✅" if start_time in selected_hours else " "
            if start_time in cheap_hours:
                line += " ⭐"
            out(line)

    def print_commands(self):
        out = self.get_io().print
        out()
        out("Komennot:")
        out()
        out("  (v) valitse ajanjakso           (esim. 'v 2022-12-23 17-18')")
        out("  (c) poista valinnat")
        out("  (g) laita merkintä kalenteriin")
        out("  (s) ohjaa Shelly-relettä        (esim. 's 0' ohjaa relettä #0)")
        out("  (q) poistu käyttöliittymästä")
        out()

    def pick(self, date, timerange):
        out = self.get_io().print
        picker = self.get_datetimepicker()
        start, end = timerange.split("-")
        out(f"Valitaan päivä {date}, ajanjakso {timerange}")
        picker.pick_between(f"{date} {start}:00", f"{date} {end}:00")

    def clear(self):
        self._datetimepicker.clear()

    def calendar(self, summary="Sähäkkä muistutus"):
        out = self.get_io().print
        msg = self.get_messageservice()
        picker = self.get_datetimepicker()
        selection = picker.to_selection()
        message = msg.create_message(
            selection, target="google-calendar", summary=summary
        )
        out(f"Viesti google-kalenteriin, payload:\n{message}")
        credentials_file = config.GOOGLE_CREDENTIALS_FILE
        if not os.path.exists(credentials_file):
            out(f"Google credentials -tiedostoa {credentials_file} ei löydy.")
            return
        if config.GOOGLE_CALENDAR_ID is None:
            out("Googlen kalenteri-id puuttuu.")
            return
        status = msg.send_message(
            message,
            credentials_file=config.GOOGLE_CREDENTIALS_FILE,
            calendar_id=config.GOOGLE_CALENDAR_ID,
        )
        out(f"Google-viesti lähetetty: {status}")
        self.clear()

    def shelly(self, relay_id):
        relay_id = int(relay_id)
        out = self.get_io().print
        msg = self.get_messageservice()
        picker = self.get_datetimepicker()
        selection = picker.to_selection()
        msg1 = msg.create_message(
            selection, target="shelly", relays=[relay_id], shift=True
        )
        out(f"Viesti Shelly-releelle, payload:\n{msg1}")
        if config.SHELLY_IP is None:
            out("Asetus SHELLY_IP puuttuu.")
        status = msg.send_message(msg1, config.SHELLY_IP)
        out(f"Shelly-viesti lähetetty: {status}")
        self.clear()

    def quit(self):
        self._done = True

    def mainloop(self):
        out = self.get_io().print
        while not self._done:
            self.list_prices()
            self.print_commands()
            line = self.get_io().input("Anna komento: ").upper()
            args = line.split(" ")
            cmd = args.pop(0)
            out()
            if cmd in self._commands:
                self._commands[cmd](*args)
            else:
                out("Virheellinen komento!")
        out("Näkemiin!")
        return 0
