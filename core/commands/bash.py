"""Команды для использования цитатника."""

from core.repositories.bashim import get_random_quote
from . import register_command
from ._libs import ResultCommandText, ResultCommand


@register_command(aliases=("bash", "баш"))
def bash(*args, **kwargs) -> ResultCommand:
    """Покажет случайную цитату с bash.im"""
    return ResultCommandText(get_random_quote())
