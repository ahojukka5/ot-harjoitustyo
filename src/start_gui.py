"""Graphical interface of saehaekkae.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
import datasources
import settings

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


def create_barchart(data):
    figure = Figure(figsize=(18, 8), dpi=100)
    axes = figure.add_subplot()
    data.energy_price.plot(kind="bar", ax=axes, picker=True)
    axes.set_title("Pörssisähkön hinta tunneittain")
    axes.set_ylabel("Hinta (c/kWh)")
    figure.autofmt_xdate(rotation=45)
    figure.tight_layout()
    return figure


def create_scheduling_widget(tab, data):
    figure = create_barchart(data)
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

    data = datasources.fetch(settings.ENERGY_PRICE_SOURCE).to_dataframe()
    data.energy_price *= 100.0

    app = tk.Tk()
    app.eval("tk::PlaceWindow . center")
    app.title("Saehaekkae - saehkoen saeaelimaetoen saeaestaejae!")
    app.geometry("800x600")

    tab_parent = ttk.Notebook(app)
    tab1 = ttk.Frame(tab_parent)
    tab2 = ttk.Frame(tab_parent)
    tab_parent.add(tab1, text="Ohjaus")
    tab_parent.add(tab2, text="Analyysi")
    tab_parent.pack(expand=1, fill="both")

    # tab 1, scheduling
    create_scheduling_widget(tab1, data)

    # tab 2, analysointi
    create_scheduling_widget(tab2, data)

    return app


if __name__ == "__main__":
    app = create_app()
    app.mainloop()
