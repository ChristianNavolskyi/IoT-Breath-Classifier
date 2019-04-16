import atexit
import logging
import os
import time
from tkinter import Tk, Scrollbar, Label, Text, StringVar, Button, N, S, W, E, END

import matplotlib
import numpy
import serial

from bounded_list import BoundedList
from classifier import Classifier
from file_logger import FileLogger
from visualiser import Visualiser

matplotlib.use('WXAgg')

breath_frequency_arg = float(os.getenv("breath_freq", 12 / 60))
scan_frequency_arg = int(os.getenv("scan_frequency", 50))
amplitude_arg = float(os.getenv("amplitude", 5.0))


class Receiver(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.wm_iconname("Breath Visualiser")
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)

        self.counter = 0

        self.x_limit = os.getenv("num_values", 100)
        self.x_values = BoundedList(self.x_limit, values=numpy.array([time.time() for _ in range(self.x_limit)]))
        self.breath_values = BoundedList(self.x_limit)

        self.value_logger = FileLogger("Breath_logger", "logs/breath.log")
        self.classifying = False
        self.classification_job = None
        self.classifier = Classifier("logs/anomalies.log", self.x_values, self.breath_values, float(os.getenv("breath_threshold", 0.25)))
        self.ser = serial.Serial()

        Label(self, text="Breath Rate").grid(row=0, column=0, pady=10)
        self.visualiser = Visualiser(self, self.x_values, self.breath_values)
        self.visualiser.grid(row=1, column=0, sticky=N + S + W)

        Label(self, text="Sensor Values").grid(row=0, column=1, pady=10)
        self.log_text = Text(self)
        self.log_text.grid(row=1, column=1, sticky=N + S + E, padx=10)

        scrollbar = Scrollbar(self, command=self.log_text.yview)
        scrollbar.grid(row=1, column=2, sticky=N + S)
        self.log_text["yscrollcommand"] = scrollbar.set

        self.button_text = StringVar(self, "Start")
        start_stop_button = Button(self,
                                   textvariable=self.button_text,
                                   command=self.on_start_stop_button,
                                   bg="grey",
                                   fg="black")
        start_stop_button.grid(row=3, columnspan=3, pady=10, sticky=S)

        self.timer_active = True
        self.isLogging = False

        atexit.register(self.do_at_exit)

    def do_at_exit(self):
        if self.ser.is_open:
            self.ser.close()

    def set_classification_state(self, state=None):
        if state is None:
            self.classifying = not self.classifying

        if self.classifying:
            self.classifier.classify_values()
            self.classification_job = self.after(1000, lambda: self.set_classification_state(True))
        elif self.classification_job is not None:
            self.after_cancel(self.classification_job)
            self.classification_job = None

    def get_sample(self, value=None, event=None, scan_frequency=50):
        if self.ser.is_open:
            sample_string = self.ser.readline()
            logging.debug("Receiving data: {0}".format(sample_string))
            value = int.from_bytes(sample_string, byteorder='big')
            logging.debug("Only number from UART: {0}".format(value))
        elif not value:
            return

        self.x_values.add_value(time.time())
        self.breath_values.add_value(value)

        self.value_logger.info("{0}".format(value))
        # self.write_log_text("Value: " + str(value))

        self.visualiser.update_plot()

        if self.counter % self.x_limit == 0 and self.counter > 0:
            self.write_log_text("Starting classification")
            self.classifier.classify_values()

        if self.timer_active:
            self.after(int(1000/20), lambda: self.get_sample(scan_frequency=scan_frequency))

    def on_start_stop_button(self):
        if not self.isLogging:
            self.isLogging = True
            self.ser.baudrate = 115200
            self.ser.timeout = 0.25
            self.ser.port = port_name
            try:
                self.ser.open()
                if self.ser.isOpen():
                    self.write_log_text("Opened port " + port_name)
                    self.button_text.set("Stop")
                    self.timer_active = True
                    self.get_sample(scan_frequency=scan_frequency_arg)
            except serial.serialutil.SerialException:
                logging.error("Could not open serial port " + str(self.ser))
        else:
            self.timer_active = False
            self.ser.close()
            self.isLogging = False
            self.button_text.set("Start")

    def write_log_text(self, message):
        self.log_text.insert(END, message + "\n")
        self.log_text.see(END)
        logging.info(message)


if __name__ == '__main__':
    port_name = os.getenv("PORT_NAME")
    if not port_name:
        logging.error("No port name provided. Please set PORT_NAME in the environment variables.")
        exit(1)

    receiver = Receiver()
    receiver.mainloop()
