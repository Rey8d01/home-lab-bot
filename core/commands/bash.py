"""Команды для использования цитатника."""

from core.repositories.bashim import get_random_quote
from . import register_command, ResultCommandText


@register_command(aliases=("bash", "баш"))
def bash(*args) -> ResultCommandText:
    """Покажет случайную цитату с bash.im"""
    return ResultCommandText(text=get_random_quote())
