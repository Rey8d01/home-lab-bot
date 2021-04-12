"""Общие команды."""

import os

import requests

from . import register_command, HELPERS_FOR_COMMANDS, ResultCommandText


@register_command
def _hello(*args, **kwargs) -> ResultCommandText:
    """Вернет 'Hello world!'."""
    return ResultCommandText("Hello world!")


@register_command
def _ping(*args, **kwargs) -> ResultCommandText:
    """Если бот работает, вернет 'Pong!'."""
    return ResultCommandText("Pong!")


@register_command(aliases=("h", "help", "помощь", "?"))
def _help(*args, **kwargs) -> ResultCommandText:
    """Покажет эту справку по командам."""
    return ResultCommandText("\n".join((f"{help_text}" for help_text in HELPERS_FOR_COMMANDS.values())))


@register_command
def _who(*args, **kwargs) -> ResultCommandText:
    """Отобразит сведения по платформе на которой запущена программа."""
    request = requests.get("https://api.ipify.org?format=json")
    white_ip = request.json()["ip"]
    name_os = os.uname()
    return ResultCommandText(f"OS: {name_os}, IP: {white_ip}")
