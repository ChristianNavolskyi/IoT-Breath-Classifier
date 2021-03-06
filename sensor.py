import logging

from serial import Serial
from serial.serialutil import SerialException

from environment_variables import port_name, baudrate, timeout, end_sequence


class Sensor(Serial):
    def __init__(self, sampling_callback, logging_callback):
        Serial.__init__(self, baudrate=baudrate, timeout=timeout)
        self.port = port_name
        self.end_sequence = end_sequence
        self.sampling = False
        self.sampling_offset = None

        self.sampling_callback = sampling_callback
        self.logging_callback = logging_callback

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
            self.logging_callback("Could not open serial port {0}".format(self))
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

        all_samples_as_bytes = sample_string.split(",".encode())[0:-1]
        string_samples = []

        if str(sample_string).startswith("b'\\x00"):
            string_samples = list(map(lambda x: str(x)[6:-1], all_samples_as_bytes))
        else:
            string_samples = list(map(lambda x: str(x)[6:-1], all_samples_as_bytes[1:-1]))
            if len(all_samples_as_bytes) > 0:
                fixed_sample = str(all_samples_as_bytes[0])[2:-1]
                string_samples[0:0] = [fixed_sample]

        int_samples = list(map(lambda x: int(x), string_samples))

        value_list = []

        for sample in int_samples:
            logging.debug("sample: {0}".format(sample))
            value_list.append(sample)

        self.sampling_callback(value_list)
