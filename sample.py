import threading
import time
import tkinter as tk

import matplotlib
import numpy
from matplotlib import style
import os

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

matplotlib.use("TkAgg")
style.use("ggplot")

def get_random_number():
    return random.randint(0, 100)


fig = Figure(figsize=(5, 5), dpi=100)
a = fig.add_subplot(1, 1, 1)
plot, = plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])


def update(arg):
    plot.set_xdata(numpy.append(plot.get_xdata(), arg))
    plot.set_ydata(numpy.append(plot.get_ydata(), get_random_number()))
    plt.draw()


def work():
    cnt = 6
    while True:
        update(cnt)
        cnt += 1
        time.sleep(0.5)


class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        canvas = FigureCanvasTkAgg(figure=fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
