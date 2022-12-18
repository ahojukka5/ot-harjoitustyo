"""Graphical interface of saehaekkae.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
import config

from services import Saehaekkae

import seaborn as sns
import pandas as pd
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter

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
    text = DateFormatter("%H").format_data(data)
    if text == "00":
        text = DateFormatter("%H\n%Y-%m-%d").format_data(data)
    return text


def create_scheduling_widget(tab, saehaekkae):

    data = saehaekkae.get_data_as_dataframe().last("3d")
    edata = _extended(data).tz_convert("Europe/Helsinki").fillna(0)
    edata.amount *= 10
    edata.price *= 100

    figure = Figure(figsize=(8, 4), dpi=100)
    axes = figure.add_subplot()

    axes.step(edata.index, edata.price, where="post", label="Hinta")
    axes.fill_between(edata.index, edata.price, step="post", alpha=0.2)
    axes.set_title("Pörssisähkön hinta tunneittain")

    axes.step(edata.index, edata.amount, where="post", label="Kulutus")
    axes.fill_between(edata.index, edata.amount, step="post", alpha=0.2)
    axes.set_ylabel("Hinta (c/kWh) | Kulutus (x100 Wh)")

    axes.xaxis.set_major_formatter(format_date)
    axes.xaxis.set_major_locator(matplotlib.dates.HourLocator(interval=3))

    xmin, xmax = edata.index[0], edata.index[-1]
    ymin, ymax = 0, axes.get_ylim()[1]
    now = datetime.datetime.utcnow()
    axes.set_ylim(ymin, ymax)
    axes.vlines(now, ymin, ymax)
    axes.set_xlim(xmin, xmax)
    axes.legend()
    figure.tight_layout()

    figure_canvas = FigureCanvasTkAgg(figure, tab)
    # NavigationToolbar2Tk(figure_canvas, self)
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def onpick(event):
        bar = event.artist
        bar.set_fc("red")
        figure.canvas.draw()

    figure.canvas.mpl_connect("pick_event", onpick)


def create_analysis_widget(tab, saehaekkae):
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
        bar = event.artist
        bar.set_fc("red")
        figure.canvas.draw()

    figure.canvas.mpl_connect("pick_event", onpick)


def create_app(saehaekkae):
    """The main Tk app."""

    app = tk.Tk()
    app.eval("tk::PlaceWindow . center")
    app.title("Saehaekkae - saehkoen saeaelimaetoen saeaestaejae!")
    app.geometry("800x600")

    tab_parent = ttk.Notebook(app)
    tab1 = ttk.Frame(tab_parent)
    tab2 = ttk.Frame(tab_parent)
    tab_parent.add(tab1, text="Hinnat")
    tab_parent.add(tab2, text="Kulutus")
    tab_parent.pack(expand=1, fill="both")

    # tab 1, show prices & scheduling
    create_scheduling_widget(tab1, saehaekkae)

    # tab 2, consumption data visualization
    create_analysis_widget(tab2, saehaekkae)

    return app


if __name__ == "__main__":
    saehaekkae = Saehaekkae()
    saehaekkae.load_db()
    app = create_app(saehaekkae)
    app.mainloop()
