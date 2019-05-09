import json
import logging
import time

import requests

from environment_variables import user_id, url
from sensor import Sensor


class Uploader:
    def __init__(self):
        self.url = url
        self.user = user_id
        self.headers = {"Content-Type": "application/json"}
        self.last_sampling = time.time()
        self.last_data = None
        self.sensor = None

    def upload_values(self, data):
        return requests.put(url=self.url + self.user, headers=self.headers, data=data)

    def sampling_callback(self, value_list):
        if self.last_sampling is None:
            self.last_sampling = time.time()
            self.last_data = value_list
        else:
            count = len(value_list)
            current_time = time.time()

            if count is not 0:
                print("Received {0} values".format(count))
                time_diff = current_time - self.last_sampling
                time_diff_per_sample = time_diff / (count + 1)
                data = []

                for index, value in enumerate(self.last_data):
                    entry = {"time": str((current_time + index * time_diff_per_sample) * 1000), "value": value}
                    data.append(entry)

                try:
                    self.upload_values(json.dumps({"breath": data}))
                except:
                    pass

            self.last_data = value_list
            self.last_sampling = current_time

            time.sleep(1)
            self.sensor.get_sample()

    def start_sampling(self):
        self.sensor = Sensor(self.sampling_callback, logging.debug)
        self.sensor.start_sampling()


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)
    Uploader().start_sampling()