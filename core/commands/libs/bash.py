"""Команды для использования цитатника."""

from core.commands.interfaces import TextCommandResult, CommandResult
from core.commands.utils import register_command
from core.repositories.bashim import get_random_quote


@register_command(aliases=("bash", "баш"))
def bash(*args, **kwargs) -> CommandResult:
    """Покажет случайную цитату с bash.im"""
    quote = get_random_quote()
    return TextCommandResult(quote if quote else "Не удалось извлечь цитату с баша")
