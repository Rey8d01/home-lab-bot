"""Команды для использования reddit."""

from core.repositories.reddit import RedditRepository
from . import register_command


@register_command
def _rrand() -> str:
    """Покажет случайный пост."""
    return RedditRepository().get_random_post()
