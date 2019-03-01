"""Команды для использования цитатника."""

from core.repositories.bashim import BashimRepository
from . import register_command


@register_command
def _bash() -> str:
    """Покажет случайную цитату с bash.im"""
    return BashimRepository().get_random_quote()
