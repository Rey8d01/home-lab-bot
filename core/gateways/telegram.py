"""Интерфейс работы с telegram.org

https://core.telegram.org/bots/api
https://github.com/eternnoir/pyTelegramBotAPI

"""

import logging
import time

import telebot

from core.commands import handle_command, ResultCommandText, ResultCommandTextPicture, \
    __dir__ as list_available_commands
from core.exceptions import UndefinedCommand
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
            try:
                result_command = handle_command(message_text)
            except UndefinedCommand:
                return

            printable_result = "Unknown result type"
            if isinstance(result_command, ResultCommandText):
                printable_result = result_command.text
            elif isinstance(result_command, ResultCommandTextPicture):
                printable_result = result_command.text
                self.telebot.send_photo(message.from_user.id, result_command.url_picture)
            self.telebot.send_message(message.from_user.id, printable_result)

        while True:
            try:
                self.telebot.polling(none_stop=True)
            except Exception as e:
                logger.debug("TM error, sleep", exc_info=e)
                time.sleep(15)
