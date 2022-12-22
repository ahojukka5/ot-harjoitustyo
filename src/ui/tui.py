import datetime
import config
import os


class IO:
    @staticmethod
    def print(*args, **kwargs):
        print(*args, **kwargs)

    @staticmethod
    def input(*args, **kwargs):
        return input(*args, **kwargs)


class TUI:
    """A simple Text User Interface"""

    def __init__(self, dataservice, datetimepicker, messageservice, io=IO):
        self._dataservice = dataservice
        self._datetimepicker = datetimepicker
        self._messageservice = messageservice
        self._io = io
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

    def list_prices(self):
        io = self.get_io()
        io.print()
        io.print("Pörssisähkön tulevat hinnat:")
        io.print()
        io.print("   ⭐   seuraavan kolmen halvimman tunnin joukossa")
        io.print("   ✅   valittu tunti")
        io.print()
        last_day = 0
        dataservice = self.get_dataservice()
        picker = self.get_datetimepicker()
        cheap_hours = dataservice.find_cheapest_hours(hours=3)
        selected_hours = picker.to_selection()
        for record in dataservice.get_future_prices():
            start = record.get_time().astimezone()
            end = start + datetime.timedelta(hours=1)
            hour = start.strftime("%H")
            next_hour = end.strftime("%H")
            date = start.strftime("%Y-%m-%d") if last_day != start.day else " " * 10
            last_day = start.day
            price = record.get_price() * 100
            s = f"{date} {hour} - {next_hour} : {price:0.2f}"
            if selected_hours.is_selected(start):
                s += " ✅"
            else:
                s += "  "
            if cheap_hours.is_selected(start):
                s += " ⭐"
            io.print(s)

    def print_commands(self):
        io = self.get_io()
        io.print()
        io.print("Komennot:")
        io.print()
        io.print("  (v) valitse ajanjakso           (esim. 'v 2022-12-23 17-18')")
        io.print("  (c) poista valinnat")
        io.print("  (g) laita merkintä kalenteriin")
        io.print("  (s) ohjaa Shelly-relettä        (esim. 's 0' ohjaa relettä #0)")
        io.print("  (q) poistu käyttöliittymästä")
        io.print()

    def pick(self, date, timerange):
        io = self.get_io()
        picker = self.get_datetimepicker()
        start, end = timerange.split("-")
        io.print(f"Valitaan päivä {date}, ajanjakso {timerange}")
        picker.pick_between(f"{date} {start}:00", f"{date} {end}:00")

    def clear(self):
        self._datetimepicker.clear()

    def calendar(self, summary="Sähäkkä muistutus"):
        io = self.get_io()
        msg = self.get_messageservice()
        picker = self.get_datetimepicker()
        selection = picker.to_selection()
        message = msg.create_message(
            selection, target="google-calendar", summary=summary
        )
        io.print(f"Viesti google-kalenteriin, payload:\n{message}")
        credentials_file = config.GOOGLE_CREDENTIALS_FILE
        if not os.path.exists(credentials_file):
            io.print(f"Google credentials -tiedostoa {credentials_file} ei löydy.")
            return
        if config.GOOGLE_CALENDAR_ID is None:
            io.print(f"Googlen kalenteri-id puuttuu.")
            return
        status = msg.send_message(
            message,
            credentials_file=config.GOOGLE_CREDENTIALS_FILE,
            calendar_id=config.GOOGLE_CALENDAR_ID,
        )
        io.print(f"Google-viesti lähetetty: {status}")
        self.clear()

    def shelly(self, relay_id):
        relay_id = int(relay_id)
        io = self.get_io()
        msg = self.get_messageservice()
        picker = self.get_datetimepicker()
        selection = picker.to_selection()
        msg1 = msg.create_message(
            selection, target="shelly", relays=[relay_id], shift=True
        )
        io.print(f"Viesti Shelly-releelle, payload:\n{msg1}")
        if config.SHELLY_IP is None:
            io.print("Asetus SHELLY_IP puuttuu.")
        status = msg.send_message(msg1, config.SHELLY_IP)
        io.print(f"Shelly-viesti lähetetty: {status}")
        self.clear()

    def quit(self):
        self._done = True

    def start(self):
        while not self._done:
            self.list_prices()
            self.print_commands()
            line = self._io.input("Anna komento: ").upper()
            args = line.split(" ")
            cmd = args.pop(0)
            self._io.print()
            if cmd in self._commands:
                self._commands[cmd](*args)
            else:
                self._io.print("Virheellinen komento!")
        self._io.print("Näkemiin!")
        return 0
