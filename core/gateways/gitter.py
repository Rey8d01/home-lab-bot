"""Интерфейс работы с gitter.im

https://developer.gitter.im/docs/welcome

"""

import json

import requests


class Gitter:
    """Gitter API."""

    def __init__(self, token: str, pre_text_message: str = ""):
        self.token = token
        self.url_rest_api = "https://api.gitter.im/v1"
        self.url_stream_api = "https://stream.gitter.im/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        self.pre_text_message = pre_text_message

    def list_rooms(self):
        """Вернет всю информацию по всем доступным комнатам."""
        url = f"{self.url_rest_api}/rooms"
        request = requests.get(url, headers=self.headers)
        return request.json()

    def send_message_in_room(self, room_id: str, text: str):
        """Отправит сообщение в комнату."""
        url = f"{self.url_rest_api}/rooms/{room_id}/chatMessages"
        payload = {"text": f"{self.pre_text_message}{text}"}
        request = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return request

    def list_messages(self, room_id: str):
        """Вернет список сообщений в комнате."""
        url = f"{self.url_rest_api}/rooms/{room_id}/chatMessages?limit=5"
        request = requests.get(url, headers=self.headers)
        return request.json()

    def listen_stream_messages(self, room_id: str):
        """Вернет генератор для стрима сообщений из указанной комнаты."""
        url = f"{self.url_stream_api}/rooms/{room_id}/chatMessages"
        request = requests.get(url, headers=self.headers, stream=True)
        if request.encoding is None:
            request.encoding = "utf-8"
        for line in request.iter_lines(decode_unicode=True):
            if line.strip():
                yield line
