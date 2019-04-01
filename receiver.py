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

        self.sample_length = 26
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
        self.visualiser.Show()
        App.MainLoop(self)

    def get_sample(self, event=None):
        sample_string = self.ser.readline()

        self.visualiser.append_log(sample_string)
        logging.debug("Receiving data: {0}".format(sample_string))

        if len(sample_string) == self.sample_length:
            sample_string = sample_string[0:-1]
            sample_values = sample_string.split()

            for m in range(self.number_of_plots):
                # get one value from sample
                value = int(sample_values[m])
                self.update_value_min_max(value)
                self.values[m][0:self.x_limit - 1] = self.values[m][1:]
                self.values[m][self.x_limit - 1] = value

            for m in range(self.number_of_plots):
                self.value_logger.info("{0}".format(self.values[m][self.x_limit - 1]))

            self.visualiser.update_plot(self.values,
                                        self.number_of_plots,
                                        self.x_limit,
                                        self.x_value_range,
                                        y_lower_limit=self.value_min - 10,
                                        y_upper_limit=self.value_max + 10)

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
            try:
                self.ser.open()
                if self.ser.isOpen():
                    message = "Opened port " + port_name
                    self.visualiser.append_log(message + "\n")
                    logging.info(message)
                    self.timer.Start(100)
                    self.visualiser.set_button_label("Stop")
            except serial.serialutil.SerialException:
                logging.error("Could not open serial port " + str(self.ser))
                pass
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

    receiver = Receiver()
    receiver.MainLoop()
