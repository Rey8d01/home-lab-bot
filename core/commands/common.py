"""Общие команды."""

import os
import time

import requests

from config import settings
from . import register_command, HELPERS_FOR_COMMANDS, PRIVATE_COMMANDS
from ._libs import TextCommandResult, CommandResult


@register_command
def hello(*args, **kwargs) -> CommandResult:
    """Покажет приветствие."""
    return TextCommandResult(f"Hi! {settings.TITLE} is online. Print help to show all commands.")


@register_command
def ping(*args, **kwargs) -> CommandResult:
    """Если бот работает, вернет 'Pong!'."""
    return TextCommandResult("Pong!")


@register_command(aliases=("h", "help", "помощь", "?"))
def _help(*args, **kwargs) -> CommandResult:
    """Покажет эту справку по доступным командам."""
    if not kwargs["is_super_user"]:
        return TextCommandResult("\n".join(f"{help_text}"
                                           for first_alias, help_text in HELPERS_FOR_COMMANDS.items()
                                           if first_alias not in PRIVATE_COMMANDS)
                                 )
    return TextCommandResult("\n".join((f"{help_text}" for help_text in HELPERS_FOR_COMMANDS.values())))


@register_command(is_private=True)
def who(*args, **kwargs) -> CommandResult:
    """Приватная функция. Отобразит сведения по платформе на которой запущена программа."""
    request = requests.get("https://api.ipify.org?format=json")
    white_ip = request.json()["ip"]
    name_os = os.uname()
    return TextCommandResult(f"OS: {name_os}, IP: {white_ip}")


@register_command(is_private=True)
def sleep(sleep_seconds: int = 5, **kwargs) -> CommandResult:
    """Приватная функция. Усыпит бота на указанное количество секунд (5 по умолчанию, макс. 60): sleep 10"""
    try:
        sleep_seconds = int(sleep_seconds)
    except ValueError:
        sleep_seconds = 5

    if 0 < sleep_seconds < 60:
        time.sleep(sleep_seconds)
    return TextCommandResult(f"{settings.TITLE} have slept enough")
