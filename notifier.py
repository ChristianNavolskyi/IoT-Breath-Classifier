import json
import logging

import requests


class Notifier:
    def __init__(self):
        self.base_url = "http://localhost:8080/"
        self.notification_url = self.base_url + "emergency/"

        try:
            requests.get(self.base_url)
            self.working = True
        except requests.exceptions.ConnectionError:
            self.working = False
            logging.warning("Telegram endpoint is not running!")

    def send_emergency(self, message=None, send_location=False):
        data = {}

        if message:
            data["message"] = str(message)

        if send_location:
            lat, lon = self.get_lon_lat()

            data[lon] = lon
            data[lat] = lat

        requests.post(self.notification_url, data=data)

    def get_lon_lat(self):
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        return (j['latitude']), (j['longitude'])
