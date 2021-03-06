"""Интерфейс работы с CLI."""

from core.commands.interfaces import TextCommandResult, TextWithPictureURLCommandResult, TextWithPictureFileCommandResult
from core.commands.utils import handle_command
from core.exceptions import UndefinedCommand, ErrorCommand
from core.gateways.interfaces import GatewayInterface


class Gateway(GatewayInterface):
    """Command Line Interface API."""

    def __init__(self, im_settings):
        self.signature_start_command = im_settings["signature_start_command"]

    def talk(self):
        print(f"Hi! Print a command, example: {self.signature_start_command}help")
        if self.signature_start_command:
            print(f"All commands start with {self.signature_start_command}")

        while True:
            message_text = str(input("#")).strip()

            if self.signature_start_command:
                if not message_text.startswith(self.signature_start_command):
                    continue
                message_text = message_text.removeprefix(self.signature_start_command)

            try:
                # CLI по дефолту считается запущенным от суперпользователя.
                result_command = handle_command(message_text, True)
            except UndefinedCommand:
                print(f"Unknown command. Press {self.signature_start_command}help to get info about available commands.")
                continue
            except ErrorCommand:
                print("Error in command. Check logs for details.")
                continue

            printable_result = "Unknown result type"
            if isinstance(result_command, TextCommandResult):
                printable_result = result_command.text
            elif isinstance(result_command, TextWithPictureURLCommandResult):
                printable_result = f"{result_command.text}, {result_command.picture_url}"
            elif isinstance(result_command, TextWithPictureFileCommandResult):
                printable_result = f"{result_command.text}, {result_command.picture_as_str}"
            print(printable_result)
