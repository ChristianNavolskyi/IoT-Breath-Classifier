from file_logger import FileLogger
from notifier import Notifier


class Classifier:
    def __init__(self):
        self.notifier = Notifier()
        self.detectionLogger = FileLogger("ANOMALY_DETECTED", "detections.log")
