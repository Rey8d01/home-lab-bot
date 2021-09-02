"""Интерфейс работы с telegram.org

https://core.telegram.org/bots/api
https://github.com/eternnoir/pyTelegramBotAPI

"""
import io
import logging
import time

import requests
import telebot
from telebot.types import Message

from core.commands import handle_command
from core.commands._libs import TextCommandResult, TextWithPictureCommandResult
from core.exceptions import UndefinedCommand, ErrorCommand
from core.gateways._libs import GatewayInterface

logger = logging.getLogger(__name__)


class Gateway(GatewayInterface):
    """Telegram API."""

    def __init__(self, im_settings):
        self.token = im_settings["token"]
        self.telebot = telebot.TeleBot(self.token)
        self.signature_start_command = im_settings["signature_start_command"]
        self.super_user_id = im_settings["super_user_id"]

    def talk(self):
        """Запускает интерфейс общения с чатом в telegram.

        Общение происходит по схеме long polling и если в процессе соединения произошли ошибки,
        то через некоторое время произойдет переподключение к telegram.

        """

        @self.telebot.message_handler()
        def message_handler(message: Message):
            message_text = str(message.text).strip()
            logger.info(f"[TM] Received message {message_text} from user {message.from_user.id}")
            is_super_user = message.from_user.id == self.super_user_id

            if self.signature_start_command:
                if not message_text.startswith(self.signature_start_command):
                    return
                message_text = message_text.removeprefix(self.signature_start_command)
            # Отдельная обработка для status как для команды которая по умолчанию есть в telegram.
            if message_text == "status":
                message_text = "help"

            try:
                result_command = handle_command(message_text, is_super_user)
            except UndefinedCommand:
                self.telebot.send_message(message.from_user.id, "Undefined command")
                return
            except ErrorCommand:
                self.telebot.send_message(message.from_user.id, "Error command")
                return

            printable_result = "Unknown result type"
            if isinstance(result_command, TextCommandResult):
                printable_result = result_command.text
            elif isinstance(result_command, TextWithPictureCommandResult):
                printable_result = result_command.text
                # Картинки требуют предварительной загрузки и отправки в бинарном виде.
                if result_command.picture_url:
                    picture = io.BytesIO(requests.get(result_command.picture_url).content)
                    self.telebot.send_photo(message.from_user.id, picture)
            self.telebot.send_message(message.from_user.id, printable_result)

        while True:
            try:
                self.telebot.polling(none_stop=True)
            except Exception as error:
                logger.debug("[TM] Connection error, sleep", exc_info=error)
                time.sleep(15)
