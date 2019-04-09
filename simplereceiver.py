import PySimpleGUI as sg

import atexit
import logging
import os
import time
from tkinter import *

import matplotlib
import numpy
import serial

from bounded_list import BoundedList
from classifier import Classifier
from file_logger import FileLogger
from visualiser import Visualiser

matplotlib.use('WXAgg')


class Receiver:
    def __init__(self):
        self.layout = [[sg.Canvas(background_color="grey"), sg.Button("Start data recording")],
                       [sg.Multiline(background_color="red")]]

        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)
        x_limit = 500
        self.sample_length = 26
        self.x_values = BoundedList(x_limit, values=numpy.array([time.time() for _ in range(x_limit)]))
        self.breath_values = BoundedList(x_limit)

        self.value_logger = FileLogger("Breath_logger", "logs/breath.log")
        self.classifier = Classifier("logs/anomalies.log", self.x_values, self.breath_values)
        self.ser = serial.Serial()

        self.visualiser = Visualiser(self, self.x_values, self.breath_values)

    def start(self):
        window = sg.Window("Breath Visualiser", default_element_size=(600, 200)).Layout(self.layout)

        while True:
            event, value = window.Read()
            print("Event: {0} Value: {1}".format(event, value))

            if event is None or event is "Exit":
                break

        window.Close()
        self.ser.close()



if __name__ == '__main__':
    rec = Receiver()
    rec.start()
