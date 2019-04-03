import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.pyplot import Figure


class Visualiser(tk.Frame):
    def __init__(self, master, x_values, *y_values):
        tk.Frame.__init__(self, master=master)

        self.x_values = x_values
        self.y_values_of_plots = y_values
        self.number_of_plots = y_values.__len__()

        fig = Figure()
        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid()

        self.ax = fig.add_subplot(1, 1, 1)

        for plot_type in range(self.number_of_plots):
            self.ax.plot(x_values.values, self.y_values_of_plots[plot_type].values)

    def update_plot(self):
        self.ax.clear()
        for plot_type in range(self.number_of_plots):
            self.ax.plot(self.x_values.values, self.y_values_of_plots[plot_type].values)

        self.canvas.draw()
