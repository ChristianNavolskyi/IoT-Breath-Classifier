from file_logger import FileLogger
from notifier import Notifier


class Classifier:
    def __init__(self, detection_file_name):
        self.notifier = Notifier()
        self.detectionLogger = FileLogger("ANOMALY_DETECTED", detection_file_name)
        self.value_size = 100

    def classify_values(self, value):
        pass
