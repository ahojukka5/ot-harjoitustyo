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

import sys
import argparse

from services import DataService, DateTimePicker, MessageService
from ui import TUI


def start_tui(args):
    print("Saehaekkae -- starting textual user interface")
    dataservice = DataService()
    dataservice.load_db()
    if not args.no_update:
        dataservice.update_db(source="spot-hinta.fi")
    datetimepicker = DateTimePicker()
    messageservice = MessageService()
    return TUI(dataservice, datetimepicker, messageservice).start()


def start_gui(args):
    print("Saehaekkae -- starting graphical user interface")
    return 0


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd", help="User interface to launch")
    subparsers.required = True
    gui = subparsers.add_parser("gui", help="Start graphical user interface")
    tui = subparsers.add_parser("tui", help="Start textual user interface")

    tui.add_argument(
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
