import requests
import json
from config import BASE_URL, COURIER_URL

class CourierMethods:
    def create_courier(self, login=None, password=None, first_name=None):
        payload = {}

        if login is not None:
            payload["login"] = login
        if password is not None:
            payload["password"] = password
        if first_name is not None:
            payload["firstName"] = first_name

        response = requests.post(f'{BASE_URL.rstrip("/")}/{COURIER_URL}', json=payload)

        if response.status_code != 201:
            return response.json()

        message = response.json().get('message')
        if message:
            message_data = json.loads(message)
            return message_data

        return response.json()

    def login_courier(self, login, password):
        data = {"login": login, "password": password}

        response = requests.post(f'{BASE_URL.rstrip("/")}/{COURIER_URL}', json=data)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.json().get("message", "Unknown error")}