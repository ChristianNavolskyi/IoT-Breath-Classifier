import logging

import requests

from environment_variables import backend_url, backend_token


class Adapter:
    def __init__(self):
        self.url = backend_url
        self.token = backend_token

    def add_data(self, record_time, value):
        if not self.token:
            logging.error("Cannot send data without access token.")
            return

        data = {"token": self.token, "time": record_time, "value": value}
        requests.post(self.url, data=data)
