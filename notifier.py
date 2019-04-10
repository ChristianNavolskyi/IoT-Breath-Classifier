import logging

import geocoder
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
            data["lon"] = lon
            data["lat"] = lat

        logging.info("Sending post")
        requests.post(self.notification_url, data=data)

    def check_endpoint_availability(self):
        try:
            requests.get(self.base_url)
            self.working = True
        except requests.exceptions.ConnectionError:
            self.working = False


def get_lon_lat():
    loc = geocoder.ip("me")
    return loc.latlng
