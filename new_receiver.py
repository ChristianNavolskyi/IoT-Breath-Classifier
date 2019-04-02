import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Receiver(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self, className="Breath Visualiser")

        fig = Figure()
        a = fig.add_subplot(1, 1, 1)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [2, 3, 1, 3, 2, 1, 3, 1])

        canvas = FigureCanvasTkAgg(figure=fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    receiver = Receiver()
    receiver.mainloop()
