"""Общие команды."""

import os

import requests

from . import register_command, COMMANDS, ResultCommandText


@register_command
def _hello(*args, **kwargs) -> ResultCommandText:
    """Вернет 'Hello world!'."""
    return ResultCommandText("Hello world!")


@register_command
def _ping(*args, **kwargs) -> ResultCommandText:
    """Если бот работает, вернет 'Pong!'."""
    return ResultCommandText("Pong!")


@register_command
def _help(*args, **kwargs) -> ResultCommandText:
    """Покажет эту справку по коммандам."""
    return ResultCommandText(
        "\n".join((f"{name_command} - {fn_command.__doc__}" for name_command, fn_command in COMMANDS.items()))
    )


@register_command
def _who(*args, **kwargs) -> ResultCommandText:
    """Отобразит сведения по платформе на которой запущена программа."""
    request = requests.get("https://api.ipify.org?format=json")
    white_ip = request.json()["ip"]
    name_os = os.uname()
    return ResultCommandText(f"OS: {name_os}, IP: {white_ip}")
