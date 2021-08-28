"""Общие команды."""

import os
import time

import requests

from . import register_command, HELPERS_FOR_COMMANDS, ResultCommandText


@register_command
def hello(*args) -> ResultCommandText:
    """Вернет 'Hello world!'."""
    return ResultCommandText("Hello world!")


@register_command
def ping(*args) -> ResultCommandText:
    """Если бот работает, вернет 'Pong!'."""
    return ResultCommandText("Pong!")


@register_command(aliases=("h", "help", "помощь", "?"))
def _help(*args) -> ResultCommandText:
    """Покажет эту справку по командам."""
    return ResultCommandText("\n".join((f"{help_text}" for help_text in HELPERS_FOR_COMMANDS.values())))


@register_command
def who(*args) -> ResultCommandText:
    """Отобразит сведения по платформе на которой запущена программа."""
    request = requests.get("https://api.ipify.org?format=json")
    white_ip = request.json()["ip"]
    name_os = os.uname()
    return ResultCommandText(f"OS: {name_os}, IP: {white_ip}")


@register_command
def sleep(*args) -> ResultCommandText:
    """Усыпит бота на указанное количество секунд (5 по умолчанию)."""
    try:
        sleep_seconds = int(args[0])
    except ValueError:
        sleep_seconds = 5
    if sleep_seconds > 0:
        time.sleep(sleep_seconds)
    return ResultCommandText(f"Get enough sleep")
