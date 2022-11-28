import tkinter as tk
import matplotlib
import datasources

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")


class App(tk.Tk):
    def __init__(self, source="test"):
        super().__init__()
        data = datasources.fetch(source)
        x = [d["DateTime"] for d in data]
        y = [100.0 * d["PriceWithTax"] for d in data]

        self.title("Saehaekkae - saehkoen saeaelimaetoen saeaestaejae!")
        figure = Figure(figsize=(18, 8), dpi=100)
        figure_canvas = FigureCanvasTkAgg(figure, self)
        # NavigationToolbar2Tk(figure_canvas, self)
        axes = figure.add_subplot()
        axes.bar(x, y)
        axes.set_title("Pörssisähkön hinta tunneittain")
        axes.set_ylabel("Hinta (c/kWh)")
        figure.autofmt_xdate(rotation=45)
        figure.tight_layout()
        figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
