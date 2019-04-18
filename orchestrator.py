import atexit
import logging
import os
from logging import INFO
from tkinter import Tk, Scrollbar, Label, Text, StringVar, Button, N, S, W, E, END

import matplotlib

from bounded_list import BoundedList
from classifier import Classifier
from environment_variables import classification_frequency, breath_threshold
from file_logger import FileLogger
from sensor import Sensor
from visualiser import Visualiser

matplotlib.use('WXAgg')


class Orchestrator(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.wm_iconname("Breath Visualiser")
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)

        self.classification_counter = 0

        self.x_limit = os.getenv("num_values", 100)
        self.x_values = BoundedList(self.x_limit)
        self.breath_values = BoundedList(self.x_limit)

        self.value_logger = FileLogger("Breath_logger", "logs/breath.log")
        self.classifying = False
        self.classification_job = None
        self.classifier = Classifier("logs/anomalies.log", self.x_values, self.breath_values, breath_threshold, self.write_log_text)

        Label(self, text="Breath Rate").grid(row=0, column=0, pady=10)
        self.visualiser = Visualiser(self, self.x_values, self.breath_values)
        self.visualiser.grid(row=1, column=0, sticky=N + S + W)

        self.sensor = Sensor(self.x_values, self.breath_values, self.sampling_callback, self.write_log_text, self.after)

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

        self.isLogging = False
        atexit.register(self.do_at_exit)

    def do_at_exit(self):
        if self.sensor.is_open:
            self.sensor.close()

    def sampling_callback(self):
        self.visualiser.update_plot()
        self.classification_counter += 1

        if self.classification_counter % classification_frequency == 0:
            self.write_log_text("Starting classification")
            self.classifier.classify_values()

    def on_start_stop_button(self):
        # TODO should work on first click
        if not self.isLogging:
            sampling_started = self.sensor.start_sampling()
            if sampling_started:
                self.isLogging = True
                self.button_text.set("Stop")
        else:
            self.isLogging = False
            self.sensor.stop_sampling()
            self.button_text.set("Start")

    def write_log_text(self, message, level=INFO):
        if level is INFO:
            self.log_text.insert(END, message + "\n")
            self.log_text.see(END)

        logging.log(level, message)


if __name__ == '__main__':
    receiver = Orchestrator()
    receiver.mainloop()
