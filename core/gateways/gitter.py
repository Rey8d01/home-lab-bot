"""Интерфейс работы с gitter.im

https://developer.gitter.im/docs/welcome

"""

import json
import logging

import requests

from core.commands import handle_command, ResultCommandText, ResultCommandTextPicture
from core.exceptions import UndefinedCommand
from core.gateways._libs import GatewayInterface

logger = logging.getLogger(__name__)


class Gateway(GatewayInterface):
    """Gitter API."""

    def __init__(self, settings_im):
        self.token = settings_im["token"]
        self.active_room = settings_im["active_room"]
        self.signature_message_bot = settings_im["signature_message_bot"]
        self.signature_start_command = settings_im["signature_start_command"]

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
            logger.debug(f"Received message: {encoded_message!r}")
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

            printable_result = "Unknown result type"
            if isinstance(result_command, ResultCommandText):
                printable_result = result_command.text
            elif isinstance(result_command, ResultCommandTextPicture):
                printable_result = f"""{result_command.text}\n![pic]({result_command.url_picture})"""
            self.send_message_in_room(self.active_room, printable_result)

    def list_rooms(self):
        """Вернет всю информацию по всем доступным комнатам."""
        url = f"{self.url_rest_api}/rooms"
        request = requests.get(url, headers=self.headers)
        return request.json()

    def send_message_in_room(self, room_id: str, text: str):
        """Отправит сообщение в комнату."""
        url = f"{self.url_rest_api}/rooms/{room_id}/chatMessages"
        payload = {"text": f"{self.signature_message_bot}\n{text}"}
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
