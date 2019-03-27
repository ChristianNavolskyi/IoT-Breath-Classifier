import logging
import os

import matplotlib
import numpy
import serial
import wx

from classifier import Classifier
from file_logger import FileLogger
from visualiser import Visualiser

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure


class Receiver(wx.Frame):
    def __init__(self):
        self.value_logger = FileLogger("Breath_logger", "breath.log")
        self.visualiser = Visualiser()
        self.classifier = Classifier()

        wx.Frame.__init__(self, None, -1, "ComPlotter", (100, 100), (640, 580))

        self.SetBackgroundColour('#ece9d8')

        # Flag variables
        self.isLogging = False

        # Create data buffers
        self.N = 100
        self.n = range(self.N)
        self.M = 5
        self.x = []
        for m in range(self.M):
            self.x.append(0 * numpy.ones(self.N, numpy.int))

        # Create plot area and axes
        self.fig = Figure(facecolor='#ece9d8')
        self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
        self.canvas.SetPosition((0, 0))
        self.canvas.SetSize((640, 320))
        self.ax = self.fig.add_axes([0.08, 0.1, 0.86, 0.8])
        self.ax.autoscale(False)
        self.ax.set_xlim(0, 99)
        self.ax.set_ylim(0, 100)
        for m in range(self.M):
            self.ax.plot(self.n, self.x[m])

        # Create text box for event logging
        self.log_text = wx.TextCtrl(
            self, -1, pos=(140, 320), size=(465, 200),
            style=wx.TE_MULTILINE)
        self.log_text.SetFont(
            wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False))

        # Create timer to read incoming data and scroll plot
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.GetSample, self.timer)

        # Create start/stop button
        self.start_stop_button = wx.Button(
            self, label="Start", pos=(25, 320), size=(100, 100))
        self.start_stop_button.SetFont(
            wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False))
        self.start_stop_button.Bind(
            wx.EVT_BUTTON, self.onStartStopButton)

    def GetSample(self, event=None):
        # Get a line of text from the serial port
        sample_string = self.ser.readline()

        # Add the line to the log text box
        self.log_text.AppendText(sample_string)

        # If the line is the right length, parse it
        if len(sample_string) == 26:
            sample_string = sample_string[0:-1]
            sample_values = sample_string.split()

            for m in range(self.M):
                # get one value from sample
                value = int(sample_values[m])
                self.x[m][0:99] = self.x[m][1:]
                self.x[m][99] = value

            # Update plot
            self.ax.cla()
            self.ax.autoscale(False)
            self.ax.set_xlim(0, self.N - 1)
            self.ax.set_ylim(-100, 1100)
            for m in range(self.M):
                self.ax.plot(self.n, self.x[m])
                self.value_logger.info("{0}".format(self.x[m]))
            self.canvas.draw()

    def onStartStopButton(self, event):
        if not self.isLogging:
            self.isLogging = True
            self.ser = serial.Serial()
            self.ser.baudrate = 115200
            self.ser.timeout = 0.25
            self.ser.port = port_name
            self.ser.open()
            if self.ser.isOpen():
                self.log_text.AppendText("Opened port " + port_name + "\n")
                # We successfully opened a port, so start
                # a timer to read incoming data
                self.timer.Start(100)
                self.start_stop_button.SetLabel("Stop")
        else:
            self.timer.Stop()
            self.ser.close()
            self.isLogging = False
            self.start_stop_button.SetLabel("Start")


if __name__ == '__main__':
    port_name = os.getenv("PORT_NAME")
    if not port_name:
        logging.error("No port name provided. Please set PORT_NAME in the environment variables.")
        exit(1)
    app = wx.App()
    window = Receiver()

    window.Show()
    app.MainLoop()
