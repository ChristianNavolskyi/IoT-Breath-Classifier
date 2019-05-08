import logging
import os

port_name = os.getenv("PORT_NAME")
if not port_name:
    logging.error("No port name provided. Please set PORT_NAME in the environment variables.")
    exit(1)

baudrate = int(os.getenv("BAUDRATE", 115200))
timeout = float(os.getenv("TIMEOUT", 0.25))
end_sequence = os.getenv("END_SEQUENCE", "Go\n").encode()
