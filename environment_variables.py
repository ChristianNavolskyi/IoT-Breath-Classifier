import logging
import os

port_name = os.getenv("PORT_NAME")
if not port_name:
    logging.error("No port name provided. Please set PORT_NAME in the environment variables.")
    exit(1)

user_id = os.getenv("USER_ID")
if not user_id:
    logging.error("No user id specified. Please set USER_ID in the environment variables.")
    exit(1)

url = os.getenv("URL", "http://localhost:5000/api/user/")
baudrate = int(os.getenv("BAUDRATE", 115200))
timeout = float(os.getenv("TIMEOUT", 0.25))
end_sequence = os.getenv("END_SEQUENCE", "Go\n").encode()
