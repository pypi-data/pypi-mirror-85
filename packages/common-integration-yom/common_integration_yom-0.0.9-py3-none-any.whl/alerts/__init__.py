import json
import sys
import random
import requests
from utils.singleton import Singleton

class Slack(metaclass=Singleton):
    def __init__(self, web_hook):
        self.web_hook = web_hook

    def send_alert(self, title, message):
        url = self.web_hook
        message = message
        title = title
        slack_data = {
            "username": "NotificationBot",
            "icon_emoji": ":satellite:",
            "channel" : "#integration-alerts",
            "attachments": [
                {
                    "color": "#9733EE",
                    "fields": [
                        {
                            "title": title,
                            "value": message,
                            "short": "false",
                        }
                    ]
                }
            ]
        }
        byte_length = str(sys.getsizeof(slack_data))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(url, data=json.dumps(slack_data), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
