import requests


class Notifier:
    def __init__(self):
        self.notification_url = "http://localhost:8080/emergency"
        requests.post(self.notification_url)
