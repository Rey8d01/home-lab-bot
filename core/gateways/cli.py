"""Интерфейс работы с CLI."""

from core.commands import handle_command
from core.exceptions import UndefinedCommand
from core.gateways._libs import GatewayInterface


class Gateway(GatewayInterface):
    """Command Line Interface API."""

    def __init__(self, settings_im):
        self.signature_start_command = settings_im["signature_start_command"]

    def talk(self):
        while True:
            message_text = str(input("#")).strip()

            if self.signature_start_command:
                if not message_text.startswith(self.signature_start_command):
                    continue
                message_text = message_text[len(self.signature_start_command):]

            try:
                result_command = handle_command(message_text)
            except UndefinedCommand:
                continue
            print(result_command)
