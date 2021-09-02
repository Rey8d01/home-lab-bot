"""Тестирование команд."""
import core.commands
import pytest

from core.commands import CommandResult
from core.exceptions import CommandException


@pytest.mark.parametrize("command", dir(core.commands))
def test_handle_command_for_super(command):
    """Тестирование базового поведения обработчика команд, который должен вернуть объект результата команды либо специальное исключение."""
    try:
        command_result = core.commands.handle_command(command, False)
        assert isinstance(command_result, CommandResult), "result command should be type of CommandResult or raise CommandException"
    except Exception as error:
        with pytest.raises(CommandException):
            raise error
