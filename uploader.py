import json
import logging
import time

import requests

from sensor import Sensor


class Uploader:
    def __init__(self):
        self.url = "http://localhost:5000/api/user/"
        self.user = "5cd2f4f7f96bbe14c2cdde2b"
        self.headers = {"Content-Type": "application/json"}
        self.last_sampling = time.time()
        self.last_data = None

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
                time_diff_per_sample = time_diff / count
                data = []

                for index, value in enumerate(self.last_data):
                    entry = {"time": str((current_time + index * time_diff_per_sample) * 1000), "value": value}
                    data.append(entry)

                self.upload_values(json.dumps({"breath": data}))

            self.last_data = value_list
            self.last_sampling = current_time

    def wait_callback(self, sensor):
        logging.debug("Waiting")
        time.sleep(5)
        sensor.get_sample()

    def start_sampling(self):
        sensor = Sensor(self.sampling_callback, logging.debug, self.wait_callback)
        sensor.start_sampling()


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)
    Uploader().start_sampling()

# class Test:
#     url = "http://localhost:5000/api/user/"
#     user = "5cc82c1d6cd4320f0edc73b5"
#     headers = {"Content-Type": "application/json"}
#
#     def generate_data(self):
#         first = time.time() * 1000
#
#         return json.dumps({
#             "breath": [{"time": str(first), "value": randint(0, 1000)}]
#         })
#
#     def put_one(self):
#         data = self.generate_data()
#         return requests.put(url=self.url + self.user, headers=self.headers, data=data)
#
#     def start(self):
#         while True:
#             try:
#                 res = self.put_one()
#             except:
#                 logging.error("Connection Error, retrying in 5 seconds")
#                 time.sleep(5)
#                 continue
#             print(res.text)
#             time.sleep(0.5)
#
#
# if __name__ == '__main__':
#     sender = Test()
#     res = sender.start()
#     print(res.text)
