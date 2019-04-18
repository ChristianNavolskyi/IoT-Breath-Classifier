import logging
from logging import ERROR

from serial import Serial
from serial.serialutil import SerialException

from environment_variables import port_name, baudrate, timeout, end_sequence


class Sensor(Serial):
    def __init__(self, x_values, y_values, sampling_callback, logging_callback, waiting_callback):
        Serial.__init__(self, port_name, baudrate, timeout=timeout)
        self.end_sequence = end_sequence
        self.x_values = x_values
        self.y_values = y_values
        self.sampling = False
        self.sampling_offset = None

        self.sampling_callback = sampling_callback
        self.logging_callback = logging_callback
        self.waiting_callback = waiting_callback

    def start_sampling(self):
        try:
            self.open()
            if self.isOpen():
                self.logging_callback("Opened port {0}".format(self.port))
                self.sampling = True
                self.get_sample()
            return True
        except SerialException:
            self.close()
            self.logging_callback("Could not open serial port {0}".format(self), ERROR)
            return False

    def stop_sampling(self):
        self.sampling = False
        self.close()
        self.logging_callback("Closed port {0}".format(self.port))

    def get_sample(self):
        if not self.is_open:
            return

        self.write(self.end_sequence)
        sample_string = self.readline()
        logging.debug("Receiving data: {0}".format(sample_string))

        separated_samples = sample_string.split(";".encode())[0:-1]
        # TODO fix first value not readable
        for sample in separated_samples:
            logging.debug("sample: {0}".format(sample))
            sample_time, sample_value = sample.split(",".encode())
            time = int(str(sample_time)[6:-1])

            if self.sampling_offset is None:
                self.sampling_offset = time

            self.x_values.add_value(time - self.sampling_offset)
            self.y_values.add_value(int(sample_value))

        self.sampling_callback()

        if self.sampling:
            self.waiting_callback(5000, lambda: self.get_sample())
