"""Команды для использования цитатника."""

from core.repositories.bashim import get_random_quote
from . import register_command
from ._libs import TextCommandResult, CommandResult


@register_command(aliases=("bash", "баш"))
def bash(*args, **kwargs) -> CommandResult:
    """Покажет случайную цитату с bash.im"""
    return TextCommandResult(get_random_quote())
