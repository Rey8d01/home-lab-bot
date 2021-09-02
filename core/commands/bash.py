"""Команды для использования цитатника."""

from core.repositories.bashim import get_random_quote
from . import register_command
from ._libs import TextCommandResult, CommandResult


@register_command(aliases=("bash", "баш"))
def bash(*args, **kwargs) -> CommandResult:
    """Покажет случайную цитату с bash.im"""
    quote = get_random_quote()
    return TextCommandResult(quote if quote else "Не удалось извлечь цитату с баша")
