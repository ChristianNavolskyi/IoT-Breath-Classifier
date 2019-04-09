import json
import logging

import requests


class Notifier:
    def __init__(self):
        self.base_url = "http://localhost:8080/"
        self.notification_url = self.base_url + "emergency/"
        self.working = False

    def send_emergency(self, message=None, send_location=False):
        self.check_endpoint_availability()

        if not self.working:
            logging.warning("Abort sending because endpoint could not be reached")
            return

        data = {}

        if message:
            data["message"] = str(message)

        if send_location:
            lat, lon = get_lon_lat()

            data[lon] = lon
            data[lat] = lat

        logging.debug("Sending post")
        requests.post(self.notification_url, data=data)

    def check_endpoint_availability(self):
        try:
            logging.debug("try pinging endpoint")
            requests.get(self.base_url)
            self.working = True
            logging.debug("endpoint available")
        except requests.exceptions.ConnectionError:
            self.working = False
            logging.warning("Telegram endpoint is not running!")


def get_lon_lat():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    return (j['latitude']), (j['longitude'])
