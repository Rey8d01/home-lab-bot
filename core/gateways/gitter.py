"""Интерфейс работы с gitter.im

https://developer.gitter.im/docs/welcome

"""

import json

import requests

from core.commands import handle_command
from core.exceptions import UndefinedCommand
from core.gateways._libs import GatewayInterface


class Gateway(GatewayInterface):
    """Gitter API."""

    def __init__(self, token: str, active_room: str, signature_message_bot: str = "",
                 signature_start_command: str = ""):
        self.token = token
        self.active_room = active_room
        self.signature_message_bot = signature_message_bot
        self.signature_start_command = signature_start_command

        self.url_rest_api = "https://api.gitter.im/v1"
        self.url_stream_api = "https://stream.gitter.im/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

    def talk(self):
        """Запускает интерфейс общения с чатом в gitter."""
        for encoded_message in self.listen_stream_messages(self.active_room):
            decoded_message = json.loads(encoded_message)
            message_text = str(decoded_message["text"]).strip()
            # Если сообщение в чате исходит от бота - пропускаем обработку.
            if message_text.startswith(self.signature_message_bot):
                continue

            if self.signature_start_command:
                if not message_text.startswith(self.signature_start_command):
                    continue
                message_text = message_text[len(self.signature_start_command):]

            try:
                result_command = handle_command(message_text)
            except UndefinedCommand:
                continue
            self.send_message_in_room(self.active_room, result_command)

    def list_rooms(self):
        """Вернет всю информацию по всем доступным комнатам."""
        url = f"{self.url_rest_api}/rooms"
        request = requests.get(url, headers=self.headers)
        return request.json()

    def send_message_in_room(self, room_id: str, text: str):
        """Отправит сообщение в комнату."""
        url = f"{self.url_rest_api}/rooms/{room_id}/chatMessages"
        payload = {"text": f"{self.pre_text_message}\n{text}"}
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
