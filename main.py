"""Запуск бота."""

import json

from core.config import settings
from core.commands import handle_command
from core.exceptions import UndefinedCommand
from core.gateways.gitter import Gitter


def listener_gitter():
    token = settings["im"]["gitter"]["token"]
    active_room = settings["im"]["gitter"]["active_room"]
    signature_message_bot = settings["im"]["gitter"]["signature_message_bot"]
    gitter = Gitter(token=token, pre_text_message=f"{signature_message_bot}\n")

    for encoded_message in gitter.listen_stream_messages(active_room):
        decoded_message = json.loads(encoded_message)
        message_text = str(decoded_message["text"]).strip()
        # Если сообщение в чате исходит от бота - пропускаем обработку.
        if message_text.startswith(signature_message_bot):
            continue

        try:
            result_command = handle_command(message_text)
        except UndefinedCommand:
            continue
        gitter.send_message_in_room(active_room, result_command)


if __name__ == "__main__":
    listener_gitter()
