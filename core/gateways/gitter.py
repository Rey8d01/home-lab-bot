"""Интерфейс работы с gitter.im

https://developer.gitter.im/docs/welcome

"""

import json
import logging

import requests

from core.commands import handle_command
from core.commands._libs import TextCommandResult, TextWithPictureCommandResult
from core.exceptions import UndefinedCommand, ErrorCommand
from core.gateways._libs import GatewayInterface

logger = logging.getLogger(__name__)


class Gateway(GatewayInterface):
    """Gitter API."""

    def __init__(self, im_settings):
        self.token = im_settings["token"]
        self.active_room = im_settings["active_room"]
        self.signature_message_bot = im_settings["signature_message_bot"]
        self.signature_start_command = im_settings["signature_start_command"]
        self.super_user_id = im_settings["super_user_id"]

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
            is_super_user = decoded_message.get("fromUser", {}).get("id", "") == self.super_user_id
            # Если сообщение в чате исходит от бота - пропускаем обработку.
            if message_text.startswith(self.signature_message_bot):
                continue

            if self.signature_start_command:
                if not message_text.startswith(self.signature_start_command):
                    continue
                message_text = message_text.removeprefix(self.signature_start_command)

            try:
                result_command = handle_command(message_text, is_super_user)
            except UndefinedCommand:
                self.send_message_in_room(self.active_room, "Undefined command")
                continue
            except ErrorCommand:
                self.send_message_in_room(self.active_room, "Error command")
                continue

            printable_result = "Unknown result type"
            if isinstance(result_command, TextCommandResult):
                printable_result = result_command.text
            elif isinstance(result_command, TextWithPictureCommandResult):
                printable_result = f"""{result_command.text}\n![pic]({result_command.picture_url})"""
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
