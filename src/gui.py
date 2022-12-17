"""Graphical interface of saehaekkae.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
from datasources import fetch_energy_price, fetch_energy_consumption
import settings

import seaborn as sns
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter

sns.set_theme()
matplotlib.use("TkAgg")


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


def create_scheduling_widget(tab, data):

    edata = _extended(data).tz_localize(None)
    price = edata["energy_price"]

    figure = Figure(figsize=(8, 4), dpi=100)
    axes = figure.add_subplot()

    axes.step(price.index, price, where="post")
    axes.fill_between(price.index, price, step="post", alpha=0.2)
    axes.set_title("Pörssisähkön hinta tunneittain")
    axes.set_ylabel("Hinta (c/kWh)")

    axes.xaxis.set_major_formatter(format_date)
    axes.xaxis.set_major_locator(matplotlib.dates.HourLocator(interval=3))

    xmin, xmax = price.index[0], price.index[-1]
    ymin, ymax = 0, axes.get_ylim()[1]
    now = pd.Timestamp.now()
    axes.set_ylim(ymin, ymax)
    axes.vlines(now, ymin, ymax)
    axes.set_xlim(xmin, xmax)
    figure.tight_layout()

    figure_canvas = FigureCanvasTkAgg(figure, tab)
    # NavigationToolbar2Tk(figure_canvas, self)
    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def onpick(event):
        bar = event.artist
        bar.set_fc("red")
        figure.canvas.draw()

    figure.canvas.mpl_connect("pick_event", onpick)


def create_analysis_widget(tab, data):
    figure = Figure(figsize=(18, 8), dpi=100)
    axes = figure.add_subplot()
    data.energy_price.tail(48).plot(kind="bar", ax=axes, picker=True)
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


def create_app():
    """The main Tk app."""

    price_data = fetch_energy_price(settings.ENERGY_PRICE_SOURCE).to_dataframe()
    price_data.energy_price *= 100.0

    consumption_data = fetch_energy_consumption(
        settings.ENERGY_CONSUMPTION_SOURCE
    ).to_dataframe()

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
    create_scheduling_widget(tab1, price_data)

    # tab 2, consumption data visualization
    create_analysis_widget(tab2, consumption_data)

    return app


if __name__ == "__main__":
    app = create_app()
    app.mainloop()
