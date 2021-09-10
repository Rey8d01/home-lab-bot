"""Тестирование команд."""
from itertools import product

import pytest

import core.commands
import core.commands.utils
from core.commands.interfaces import CommandResult
from core.exceptions import CommandException


@pytest.mark.parametrize("command, is_super_user", product(dir(core.commands), (True, False)))
def test_handle_command_for_user(mocker, command: str, is_super_user: bool):
    """Тестирование базового поведения обработчика для всех команд.

    Всякая команда должна вернуть объект результата команды либо специальное исключение.
    Все "долгие" зависимые функции мокаются.

    """
    mocker.patch("time.sleep")
    mocker.patch("core.repositories.reddit.RedditRepository.get_random_latest_post_by_subreddit")
    mocker.patch("core.repositories.bashim.get_random_quote")
    mocker.patch("requests.get")
    try:
        command_result = core.commands.utils.handle_command(command, is_super_user)
        assert isinstance(command_result, CommandResult), "result command should be type of CommandResult or raise CommandException"
    except Exception as error:
        with pytest.raises(CommandException):
            raise error
