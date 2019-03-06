"""Интерфейс работы с telegram.org

https://core.telegram.org/bots/api
https://github.com/eternnoir/pyTelegramBotAPI

"""

import logging
import time

import telebot

from core.commands import handle_command
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

        @self.telebot.message_handler(content_types=['text'])
        def message_handler(message):
            message_text = str(message.text).strip()
            try:
                result_command = handle_command(message_text)
                self.telebot.send_message(message.from_user.id, result_command)
            except UndefinedCommand:
                pass

        while True:
            try:
                self.telebot.polling(none_stop=True)
            except Exception as e:
                logger.debug("TM error, sleep", exc_info=e)
                time.sleep(15)
