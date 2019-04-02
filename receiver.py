import atexit
import logging
import os
from tkinter import *

import matplotlib
import numpy
import serial

from bounded_list import BoundedList
from classifier import Classifier
from file_logger import FileLogger
from visualiser import Visualiser

matplotlib.use('WXAgg')


def sin(frequency, sin_amplitude, x):
    return sin_amplitude * numpy.sin(x * 2 * numpy.pi / frequency) + sin_amplitude


breath_frequency = float(os.getenv("breath_freq", 12 / 60))
scan_frequency = int(os.getenv("scan_freq", 500))
amplitude = float(os.getenv("amplitude", 5.0))


class Receiver(Tk):
    def __init__(self):
        Tk.__init__(self, className="Breath Visualiser")
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

        self.counter = 0

        x_limit = 10
        self.sample_length = 26
        self.x_value_range = range(x_limit)
        self.values = BoundedList(x_limit)

        self.visualiser = Visualiser(self, 1, [self.values], self.x_value_range)
        self.visualiser.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        self.button_text = StringVar(self, "Start")
        start_stop_button = Button(self,
                                   textvariable=self.button_text,
                                   command=self.on_start_stop_button,
                                   bg="grey",
                                   fg="black")
        start_stop_button.pack(side=BOTTOM, fill=X, expand=True, padx=10, pady=10)

        self.log_text = Text(self)
        self.log_text.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        self.value_logger = FileLogger("Breath_logger", "breath.log")
        self.classifier = Classifier()
        self.ser = serial.Serial()

        self.timer_active = True
        self.isLogging = False

        atexit.register(self.do_at_exit)

    def do_at_exit(self):
        if self.ser.is_open:
            self.ser.close()

    def get_sample(self, value=None, event=None):
        if self.ser.is_open:
            sample_string = self.ser.readline()
            self.log_text.insert(END, str(sample_string) + "\n")
            logging.debug("Receiving data: {0}".format(sample_string))

            if len(sample_string) == self.sample_length:
                sample_string = sample_string[0:-1]
                sample_values = sample_string.split()
                value = int(sample_values[0])
        elif not value:
            return

        self.values.add_value(value)
        self.value_logger.info("{0}".format(value))

        self.visualiser.update_plot([self.values], 1, self.x_value_range)

        if self.timer_active:
            self.after(10, self.get_sample)

    def simulate_sample(self):
        print(self.counter)
        self.timer_active = False
        x = self.counter * 1 / scan_frequency
        self.get_sample(value=sin(breath_frequency, amplitude, x))
        self.after(500, func=self.simulate_sample)
        self.counter += 1

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
                    self.log_text.insert(END, message + "\n")
                    logging.info(message)
                    self.button_text.set("Stop")
                    self.timer_active = True
                    self.get_sample()
            except serial.serialutil.SerialException:
                logging.error("Could not open serial port " + str(self.ser))
        else:
            self.timer_active = False
            self.ser.close()
            self.isLogging = False
            self.button_text.set("Start")


if __name__ == '__main__':
    port_name = os.getenv("PORT_NAME")
    if not port_name:
        logging.error("No port name provided. Please set PORT_NAME in the environment variables.")
        exit(1)

    receiver = Receiver()
    receiver.mainloop()
