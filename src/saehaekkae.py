"""Saehaekkae is a program to help reduce user's energy bill.

In a variable-price electricity contract, the user can save on the total price
of energy by scheduling the use of electricity for favorable periods. Saehaekkae
tackles this problem basically from two different starting points.

1) by scheduling the use of the devices either automatically (for example with
various wifi relays) or by receiving a message about the favorable usage time to
a smart device

2) by understanding your own electricity consumption over time by visually
looking at graphs and calculating certain key figures (how well did I manage to
optimize?)
"""

import os
import sys
import argparse

import config
from services import DataService, DateTimePicker, MessageService
from ui import TUI, GUI


def update_sources(dataservice):
    """Update sources."""
    print("Updating prices")
    source_name = config.ENERGY_PRICE_SOURCE
    source = dataservice.get_source(source_name)
    price, amount = dataservice.update_db(source)
    print(f"Updated {price} price information")
    source_name = config.ENERGY_CONSUMPTION_SOURCE
    local_file = config.ENERGY_CONSUMPTION_FILE
    if os.path.exists(local_file):
        source = dataservice.get_source(source_name, local_file=local_file)
        price, amount = dataservice.update_db(source)
        print(f"Updated {amount} consumption information from local file {local_file}")
    else:
        print(f"Failed to update consumption: file {local_file} does not exist")


def start_tui(args):
    """Saehaekkae textual user interface starting command."""
    print("Saehaekkae -- starting textual user interface")
    dataservice = DataService()
    dataservice.load_db(config.DB_FILE)
    if not args.no_update:
        update_sources(dataservice)
    datetimepicker = DateTimePicker()
    messageservice = MessageService()
    return TUI(dataservice, datetimepicker, messageservice).mainloop()


def start_gui(args):
    """Saehaekkae graphical user interface starting command."""
    print("Saehaekkae -- starting graphical user interface")
    dataservice = DataService()
    dataservice.load_db(config.DB_FILE)
    if not args.no_update:
        update_sources(dataservice)
    datetimepicker = DateTimePicker()
    messageservice = MessageService()
    return GUI(dataservice, datetimepicker, messageservice).mainloop()


def main():
    """Saehaekkae main entry point."""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd", help="User interface to launch")
    subparsers.required = True
    gui = subparsers.add_parser("gui", help="Start graphical user interface")
    tui = subparsers.add_parser("tui", help="Start textual user interface")

    parser.add_argument(
        "--no-update",
        help="don't update prices automatically from api.spot-hinta.fi",
        action="store_true",
    )

    gui.set_defaults(func=start_gui)
    tui.set_defaults(func=start_tui)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
