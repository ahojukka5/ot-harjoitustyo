"""Graphical interface of saehaekkae.
"""

import tkinter as tk
import matplotlib
import datasources

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


class App(tk.Tk):
    """The main Tk app."""

    def __init__(self, source="spot-hinta.fi"):
        super().__init__()
        data = datasources.fetch(source).to_dataframe()
        data.energy_price *= 100.0

        self.title("Saehaekkae - saehkoen saeaelimaetoen saeaestaejae!")
        figure = Figure(figsize=(18, 8), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        # NavigationToolbar2Tk(figure_canvas, self)
        axes = figure.add_subplot()
        data.energy_price.plot(kind="bar", ax=axes, picker=True)
        axes.set_title("Pörssisähkön hinta tunneittain")
        axes.set_ylabel("Hinta (c/kWh)")
        figure.autofmt_xdate(rotation=45)
        figure.tight_layout()
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        def onpick(event):
            bar = event.artist
            bar.set_fc("red")
            figure.canvas.draw()

        figure.canvas.mpl_connect("pick_event", onpick)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
