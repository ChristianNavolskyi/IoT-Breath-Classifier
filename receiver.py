import logging
import os

import matplotlib
import serial
import wx
from wx import App

from bounded_list import BoundedList
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
        self.values = BoundedList(self.x_limit)

        self.value_logger = FileLogger("Breath_logger", "breath.log")
        self.visualiser = Visualiser(self.on_start_stop_button, 1, [self.values], self.x_limit, self.x_value_range)
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
            value = int(sample_values[0])

            self.values.add_value(value)
            self.value_logger.info("{0}".format(value))
    
            self.visualiser.update_plot([self.values],
                                        1,
                                        self.x_limit,
                                        self.x_value_range,
                                        y_lower_limit=self.values.max() - 10,
                                        y_upper_limit=self.values.min() + 10)

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
