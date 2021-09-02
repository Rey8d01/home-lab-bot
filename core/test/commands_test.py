"""Тестирование команд."""
import pytest

import core.commands
from core.commands import CommandResult
from core.exceptions import CommandException


@pytest.mark.parametrize("command", dir(core.commands))
def test_handle_command_for_super(command, mocker):
    """Тестирование базового поведения обработчика для всех команд.

    Всякая команда должна вернуть объект результата команды либо специальное исключение.
    Все "долгие" зависимые функции мокаются.

    """
    mocker.patch("time.sleep")
    mocker.patch("core.repositories.reddit.RedditRepository.get_random_latest_post_by_subreddit")
    mocker.patch("core.repositories.bashim.get_random_quote")
    try:
        command_result = core.commands.handle_command(command, True)
        assert isinstance(command_result, CommandResult), "result command should be type of CommandResult or raise CommandException"
    except Exception as error:
        with pytest.raises(CommandException):
            raise error
