"""Команды для использования цитатника."""

from core.repositories.bashim import BashimRepository
from . import register_command, ResultCommandText


@register_command(aliases=("bash", "баш"))
def bash(*args) -> ResultCommandText:
    """Покажет случайную цитату с bash.im"""
    return ResultCommandText(text=BashimRepository().get_random_quote())
