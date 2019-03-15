"""Команды для использования reddit."""

from core.repositories.reddit import RedditRepository
from . import register_command, ResultCommandTextPicture


@register_command(aliases=("r", "reddit", "р", "реддит"))
def _reddit(*args, **kwargs) -> ResultCommandTextPicture:
    """Покажет случайный пост."""
    name_subreddit, url_post, title_post, url_picture = RedditRepository().get_random_latest_post()
    return ResultCommandTextPicture(text=f"[{name_subreddit}] {title_post} {url_post}", url_picture=url_picture)
