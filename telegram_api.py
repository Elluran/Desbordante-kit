import requests
import config

def api_request(method: str, *, data: dict = None, json: str = None, files = None):
    return requests.post(f"https://api.telegram.org/bot{config.bot_token}/{method}",
                             json=json, data=data, files=files).json()


def send_message(user_id, *, message):
    """sends message to user via telegram"""

    params = {"chat_id": int(user_id), "text": message}

    api_request(method="sendMessage", json=params)

def send_document(user_id, filename):
    """sends document to user via telegram"""

    document = open(filename, 'rb')
    params = {"chat_id": int(user_id)}

    api_request(method="sendDocument", data=params, files={'document': document})

