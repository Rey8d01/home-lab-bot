"""Интерфейс работы с gitter.im

https://developer.gitter.im/docs/welcome

"""

import json

import requests


class Gitter:
    """Gitter API."""

    def __init__(self, token: str, url_api: str = None, pre_text_message: str = ""):
        self.token = token
        self.url_api = url_api or "https://api.gitter.im/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        self.pre_text_message = pre_text_message

    def list_rooms(self):
        """Вернет всю информацию по всем доступным комнатам"""
        request = requests.get(f"{self.url_api}/rooms", headers=self.headers)
        return request.json()

    def send_message_in_room(self, room_id: str, text: str):
        """Отправит сообщение в комнату."""
        url = f"{self.url_api}/rooms/{room_id}/chatMessages"
        payload = {"text": f"{self.pre_text_message}{text}"}
        request = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return request
