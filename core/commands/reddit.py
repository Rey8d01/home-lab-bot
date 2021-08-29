"""Команды для использования reddit."""

import random

from config import settings
from core.repositories.reddit import RedditRepository
from . import register_command, ResultCommandTextPicture, ResultCommandText

DEFAULT_SUBREDDIT = "all"  # Если интересные сабреддиты в конфиге не указаны, будет использован этот.


@register_command(aliases=("r", "reddit", "р", "реддит"))
def reddit(raw_subreddit: str = None) -> ResultCommandTextPicture:
    """Покажет случайный пост по указанному сабреддиту или по случайному заданному в настройках."""
    interesting_subreddit = raw_subreddit
    if not interesting_subreddit:
        interesting_subreddit = random.choice(settings.REPOS.REDDIT.SUBS) if settings.REPOS.REDDIT.SUBS else DEFAULT_SUBREDDIT

    post_url, post_title, picture_url = RedditRepository().get_random_latest_post_by_subreddit(interesting_subreddit)
    post_text = f"[{interesting_subreddit}] {post_title} {post_url}"
    return ResultCommandTextPicture(text=post_text, picture_url=picture_url) if picture_url else ResultCommandText(text=post_text)
