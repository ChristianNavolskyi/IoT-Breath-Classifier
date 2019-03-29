import logging
import os

import matplotlib
import numpy
import serial
import wx
from wx import App

from classifier import Classifier
from file_logger import FileLogger
from visualiser import Visualiser

matplotlib.use('WXAgg')


class Receiver(App):
    def __init__(self):
        App.__init__(self)

        self.x_limit = 100
        self.x_value_range = range(self.x_limit)
        self.number_of_plots = 1
        self.values = []
        for m in range(self.number_of_plots):
            self.values.append(0 * numpy.ones(self.x_limit, numpy.int))

        self.value_extremes = [0 for _ in self.x_value_range]
        self.value_max = float("-inf")
        self.value_min = float("inf")

        self.value_logger = FileLogger("Breath_logger", "breath.log")
        self.visualiser = Visualiser(self.on_start_stop_button, self.number_of_plots, self.values, self.x_limit, self.x_value_range)
        self.classifier = Classifier()
        self.ser = serial.Serial()
        self.timer = wx.Timer(self)

        self.Bind(wx.EVT_TIMER, self.get_sample, self.timer)
        self.isLogging = False

    def MainLoop(self):
        App.MainLoop(self)
        self.visualiser.show()

    def get_sample(self, event=None):
        # Get a line of text from the serial port
        sample_string = self.ser.readline()

        # Add the line to the log text box
        self.visualiser.append_log(sample_string)

        # If the line is the right length, parse it
        if len(sample_string) == 26:
            sample_string = sample_string[0:-1]
            sample_values = sample_string.split()

            for m in range(self.number_of_plots):
                # get one value from sample
                value = int(sample_values[m])
                self.update_value_min_max(value)
                self.values[m][0:99] = self.values[m][1:]
                self.values[m][99] = value

            for m in range(self.number_of_plots):
                self.value_logger.info("{0}".format(self.values[m]))

            self.visualiser.update_plot(self.values, self.number_of_plots, self.x_limit, self.x_value_range, y_lower_limit=self.value_min - 10, y_upper_limit=self.value_max + 10)
            # Update plot
            # self.ax.cla()
            # self.ax.autoscale(False)
            # self.ax.set_xlim(0, self.N - 1)
            # self.ax.set_ylim(-100, 1100)
        # self.canvas.draw()

    def update_value_min_max(self, value):
        self.value_extremes[0:self.x_limit - 1] = self.value_extremes[1:]
        self.value_extremes[self.x_limit - 1] = value

        self.value_max = max(self.value_extremes)
        self.value_min = min(self.value_extremes)

    def on_start_stop_button(self, event):
        if not self.isLogging:
            self.isLogging = True
            self.ser.baudrate = 115200
            self.ser.timeout = 0.25
            self.ser.port = port_name
            self.ser.open()
            if self.ser.isOpen():
                self.visualiser.append_log("Opened port " + port_name + "\n")
                # We successfully opened a port, so start
                # a timer to read incoming data
                self.timer.Start(100)
                self.visualiser.set_button_label("Stop")
        else:
            self.timer.Stop()
            self.ser.close()
            self.isLogging = False
            self.visualiser.set_button_label("Start")


if __name__ == '__main__':
    port_name = os.getenv("PORT_NAME")
    if not port_name:
        logging.error("No port name provided. Please set PORT_NAME in the environment variables.")
        exit(1)
    app = wx.App()
    window = Receiver()

    window.Show()
    app.MainLoop()
