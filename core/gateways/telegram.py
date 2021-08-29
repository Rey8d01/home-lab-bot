"""Интерфейс работы с telegram.org

https://core.telegram.org/bots/api
https://github.com/eternnoir/pyTelegramBotAPI

"""
import io
import logging
import time

import requests
import telebot

from core.commands import handle_command, ResultCommandText, ResultCommandTextPicture, \
    __dir__ as list_available_commands
from core.exceptions import UndefinedCommand, ErrorCommand
from core.gateways._libs import GatewayInterface

logger = logging.getLogger(__name__)


class Gateway(GatewayInterface):
    """Telegram API."""

    def __init__(self, settings_im):
        self.token = settings_im["token"]
        self.telebot = telebot.TeleBot(self.token)

    def talk(self):
        """Запускает интерфейс общения с чатом в telegram."""

        @self.telebot.message_handler(commands=list_available_commands())
        def message_handler(message):
            message_text = str(message.text).strip()
            # Для обработки конкретного списка комманд первым символом из tm приходит / всегда.
            message_text = message_text[1:]
            try:
                result_command = handle_command(message_text)
            except UndefinedCommand:
                return
            except ErrorCommand:
                return

            printable_result = "Unknown result type"
            if isinstance(result_command, ResultCommandText):
                printable_result = result_command.text
            elif isinstance(result_command, ResultCommandTextPicture):
                printable_result = result_command.text
                # Картинки требуют предварительной загрузки и отправки в бинарном виде.
                if result_command.picture_url:
                    picture = io.BytesIO(requests.get(result_command.picture_url).content)
                    self.telebot.send_photo(message.from_user.id, picture)
            self.telebot.send_message(message.from_user.id, printable_result)

        while True:
            try:
                self.telebot.polling(none_stop=True)
            except Exception as e:
                logger.debug("TM error, sleep", exc_info=e)
                time.sleep(15)
