import json
import logging
import time
from random import randint

import requests


class Test:
    url = "http://localhost:5000/api/user/"
    user = "5cc82c1d6cd4320f0edc73b5"
    headers = {"Content-Type": "application/json"}

    def generate_data(self):
        first = time.time() * 1000

        return json.dumps({
            "breath": [{"time": str(first), "value": randint(0, 1000)}]
        })

    def put_one(self):
        data = self.generate_data()
        return requests.put(url=self.url + self.user, headers=self.headers, data=data)

    def start(self):
        while True:
            try:
                res = self.put_one()
            except:
                logging.error("Connection Error, retrying in 5 seconds")
                time.sleep(5)
                continue
            print(res.text)
            time.sleep(0.5)


if __name__ == '__main__':
    sender = Test()
    res = sender.start()
    print(res.text)
