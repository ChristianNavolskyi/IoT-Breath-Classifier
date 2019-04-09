import logging

import numpy as np

from file_logger import FileLogger
from notifier import Notifier


class Classifier:
    def __init__(self, detection_file_name, time_values, breath_values, threshold):
        self.notifier = Notifier()
        self.detectionLogger = FileLogger("ANOMALY_DETECTED", detection_file_name)

        self.time_values = time_values
        self.breath_values = breath_values

        self.initial_breath_rate = None
        self.threshold = threshold

    def classify_values(self):
        time = self.time_values.copy_values()
        breath = self.breath_values.copy_values()

        breath_mean = np.mean(breath)
        time_crossing_values = np.argwhere(np.diff(np.sign(breath - breath_mean))).flatten()

        crossing_times = time[time_crossing_values]
        logging.info("Crossing Times: {0}".format(crossing_times))

        diffs = np.diff(crossing_times)
        logging.info("Diffs: {0}".format(diffs))

        mean_diff = np.mean(diffs)
        logging.info("Mean diff: {0}".format(mean_diff))

        if self.initial_breath_rate is None:
            self.initial_breath_rate = mean_diff
        elif mean_diff / self.initial_breath_rate < 1 - self.threshold:
            self.notifier.send_emergency("An asthma attack could be happening right now, please help", send_location=True)
