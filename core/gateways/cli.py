"""Интерфейс работы с CLI."""

from core.commands import handle_command
from core.exceptions import UndefinedCommand
from core.gateways._libs import GatewayInterface


class Gateway(GatewayInterface):
    """Command Line Interface API."""

    def __init__(self):
        pass

    def talk(self):
        while True:
            message_text = str(input("#")).strip()
            try:
                result_command = handle_command(message_text)
            except UndefinedCommand:
                continue
            print(result_command)
