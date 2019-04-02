import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
from wx import Frame, EVT_SIZE


class Visualiser(Frame):
    def __init__(self, start_button_callback, number_of_plots, values, x_limit, x_value_range, y_limit=100, width=640, height=640):
        Frame.__init__(self, None, -1, "ComPlotter", size=(width, height))
        self.SetBackgroundColour("#ece9d8")

        self.display_margin = 20
        self.button_height = 50
        height_for_displays = (height - self.button_height) / 2

        self.fig = Figure(facecolor='#ece9d8')
        self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
        self.ax = self.fig.add_axes([0.08, 0.1, 0.86, 0.8])
        self.ax.autoscale(False)
        self.ax.set_xlim(0, x_limit - 1)
        self.ax.set_ylim(0, y_limit)

        for m in range(number_of_plots):
            self.ax.plot(x_value_range, values[m].values)

        self.log_text = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        self.log_text.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False))

        self.start_stop_button = wx.Button(self, label="Start")
        self.start_stop_button.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False))
        self.start_stop_button.Bind(wx.EVT_BUTTON, start_button_callback)

        self.Bind(event=EVT_SIZE, handler=self.update_size)
        self.Show()

    def update_size(self, event):
        width, height = event.GetSize()
        height_for_displays = (height - self.button_height) / 2

        self.canvas.SetPosition((self.display_margin, self.display_margin))
        self.canvas.SetSize((width - 2 * self.display_margin, height_for_displays - 2 * self.display_margin))

        self.log_text.SetPosition((self.display_margin, height_for_displays + self.button_height))
        self.log_text.SetSize((width - 2 * self.display_margin, height_for_displays - 2 * self.display_margin))

        self.start_stop_button.SetPosition(((width - 100) / 2, height_for_displays))
        self.start_stop_button.SetSize((100, 50))

    def set_button_label(self, label):
        self.start_stop_button.SetLabel(label)

    def update_plot(self, values, number_of_plots=1, x_limit=100, x_value_range=100, y_lower_limit=0, y_upper_limit=100):
        self.ax.cla()
        self.ax.autoscale(False)
        self.ax.set_xlim(0, x_limit - 1)
        self.ax.set_ylim(y_lower_limit, y_upper_limit)

        for plot_type in range(number_of_plots):
            self.ax.plot(x_value_range, values[plot_type].values)

        self.canvas.draw()

    def append_log(self, text):
        self.log_text.AppendText(text)
