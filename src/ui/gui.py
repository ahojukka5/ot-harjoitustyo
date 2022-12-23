"""Graphical interface of saehaekkae.
"""


import tkinter as tk
from tkinter import ttk
import math
import datetime
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
import seaborn as sns
import pandas as pd

sns.set_theme()
matplotlib.use("TkAgg")
matplotlib.rcParams["timezone"] = "Europe/Helsinki"


def _extended(data):
    lastrow = pd.DataFrame(
        index=[data.index[-1] + pd.Timedelta("1h")],
        data=data.tail(1).values,
        columns=data.columns,
    )
    return pd.concat([data, lastrow])


def format_date(data, _):
    """Matplotlib formatter for datetime. Every midnight give additional date information."""
    text = DateFormatter("%H").format_data(data)
    if text == "00":
        text = DateFormatter("%H\n%Y-%m-%d").format_data(data)
    return text


def _prepare_data(dataservice):
    data = dataservice.get_data_as_dataframe().dropna(how="all").last("4d")
    edata = _extended(data).tz_convert("Europe/Helsinki").fillna(0)
    edata.price *= 100
    scaling = edata.price.max() / edata.amount.max()
    scaling = math.floor(scaling)
    edata.amount *= scaling
    return edata, scaling


def _format_axes(axes, scaling=1):
    axes2 = axes.twinx()
    axes2.grid()
    axes2.set_ylabel("Kulutus (kWh)")

    axes.xaxis.set_major_formatter(format_date)
    axes.xaxis.set_major_locator(matplotlib.dates.HourLocator(interval=3))

    yticks = []
    for tick in axes.get_yticks():
        y_value = tick / scaling
        yticks.append(f"{y_value:0.2f}")
    axes2.set_yticks(axes.get_yticks())
    axes2.set_yticklabels(yticks)

    axes.set_ylim(0, axes.get_ylim()[1])
    axes2.set_ylim(0, axes.get_ylim()[1])


def create_scheduling_widget(tab, dataservice):
    """Return scheduling widget (tab 1)."""

    data, scaling = _prepare_data(dataservice)

    figure = Figure(figsize=(19.20, 5.40), dpi=100)
    axes = figure.add_subplot()

    axes.step(data.index, data.price, where="post", label="Hinta")
    axes.fill_between(data.index, data.price, step="post", alpha=0.2)
    axes.set_title("Pörssisähkön hinta tunneittain")

    axes.step(data.index, data.amount, where="post", label="Kulutus")
    axes.fill_between(data.index, data.amount, step="post", alpha=0.2)
    axes.set_ylabel("Hinta (c/kWh)")

    _format_axes(axes, scaling=scaling)

    xmin, xmax = data.index[0], data.index[-1]
    axes.vlines(datetime.datetime.utcnow(), 0, axes.get_ylim()[1])
    axes.set_xlim(xmin, xmax)
    axes.legend()
    figure.tight_layout()

    figure_canvas = FigureCanvasTkAgg(figure, tab)
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def create_analysis_widget(tab, saehaekkae):
    """Create analysis widged (tab 2)."""
    data = saehaekkae.get_data_as_dataframe()
    figure = Figure(figsize=(18, 8), dpi=100)
    axes = figure.add_subplot()
    data.price.tail(48).plot(kind="bar", ax=axes, picker=True)
    axes.set_title("Sähkön käyttö tunneittain")
    axes.set_ylabel("Määrä (kWh)")
    figure.autofmt_xdate(rotation=45)
    figure.tight_layout()

    figure_canvas = FigureCanvasTkAgg(figure, tab)
    # NavigationToolbar2Tk(figure_canvas, self)
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def onpick(event):
        event.artist.set_fc("red")
        figure.canvas.draw()

    figure.canvas.mpl_connect("pick_event", onpick)


class GUI(tk.Tk):
    """Saehaekkae graphical user interface class."""

    def __init__(self, dataservice, datetimepicker, messageservice):
        super().__init__()
        self._dataservice = dataservice
        self._datetimepicker = datetimepicker
        self._messageservice = messageservice
        # self.eval("tk::PlaceWindow . center")
        self.title("Saehaekkae - saehkoen saeaelimaetoen saeaestaejae!")
        # self.geometry("2400x1200")

        tab_parent = ttk.Notebook(self)
        tab1 = ttk.Frame(tab_parent)
        tab2 = ttk.Frame(tab_parent)
        tab_parent.add(tab1, text="Hinnat")
        tab_parent.add(tab2, text="Kulutus")
        tab_parent.pack(expand=1, fill="both")

        # tab 1, show prices & scheduling
        create_scheduling_widget(tab1, dataservice)

        # tab 2, consumption data visualization
        create_analysis_widget(tab2, dataservice)
