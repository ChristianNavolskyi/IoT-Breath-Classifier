import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure


class Visualiser(tk.Frame):
    def __init__(self, master, number_of_plots, values, x_value_range):
        tk.Frame.__init__(self, master=master)

        fig = Figure()
        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.ax = fig.add_subplot(1, 1, 1)

        for m in range(number_of_plots):
            self.ax.plot(x_value_range, values[m].values)

    def update_plot(self, values, number_of_plots=1, x_value_range=range(100)):
        self.ax.clear()

        for plot_type in range(number_of_plots):
            self.ax.plot(x_value_range, values[plot_type].values)

        self.canvas.draw()
