"""Интерфейс работы с CLI."""

from core.commands import handle_command, ResultCommandText, ResultCommandTextPicture
from core.exceptions import UndefinedCommand, ErrorCommand
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
                print(f"Unknown command. Press {self.signature_start_command}help to get info about available commands.")
                continue
            except ErrorCommand:
                print(f"Error in command. Check logs for details.")
                continue

            printable_result = "Unknown result type"
            if isinstance(result_command, ResultCommandText):
                printable_result = result_command.text
            elif isinstance(result_command, ResultCommandTextPicture):
                printable_result = f"{result_command.text}, {result_command.picture_url}"
            print(printable_result)
