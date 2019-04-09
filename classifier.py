import logging

import numpy as np

from file_logger import FileLogger
from notifier import Notifier


class Classifier:
    def __init__(self, detection_file_name, time_values, breath_values):
        self.notifier = Notifier()
        self.detectionLogger = FileLogger("ANOMALY_DETECTED", detection_file_name)

        self.time_values = time_values
        self.breath_values = breath_values

    def classify_values(self):
        time = self.time_values.copy()
        breath = self.breath_values.copy()

        breath_mean = np.mean(breath)

        time_crossing_values = np.argwhere(np.diff(np.sign(breath - breath_mean))).flatten()

        crossing_times = time[time_crossing_values]
        logging.info("Crossing Times: {0}".format(crossing_times))

        diffs = np.diff(crossing_times)
        logging.info("Diffs: {0}".format(diffs))

        mean_diff = np.mean(diffs)
        logging.info("Mean diff: {0}".format(mean_diff))

        classification_result = False

        if classification_result:
            self.notifier.send_emergency("An asthma attack could be happening right now, please help", send_location=True)
