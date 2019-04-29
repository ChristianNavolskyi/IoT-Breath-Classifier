import logging
import os

port_name = os.getenv("PORT_NAME")
if not port_name:
    logging.error("No port name provided. Please set PORT_NAME in the environment variables.")
    exit(1)

baudrate = int(os.getenv("BAUDRATE", 115200))
timeout = float(os.getenv("TIMEOUT", 0.25))
end_sequence = os.getenv("END_SEQUENCE", "end").encode()
num_values = os.getenv("num_values", 200)
y_upper_limit = os.getenv("y_upper_limit", 1000000)
classification_frequency = int(os.getenv("classification_frequency", 5))
breath_threshold = float(os.getenv("breath_threshold", 0.25))
