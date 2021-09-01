"""Команды для использования reddit."""

import random

from config import settings
from core.repositories.reddit import RedditRepository
from . import register_command
from ._libs import ResultCommandText, ResultCommandTextPicture, ResultCommand

DEFAULT_SUBREDDIT = "all"  # Если интересные сабреддиты в конфиге не указаны, будет использован этот.
reddit_repository = RedditRepository()


@register_command(aliases=("r", "reddit", "р", "реддит"))
def reddit(raw_subreddit: str, **kwargs) -> ResultCommand:
    """Покажет случайный пост по указанному сабреддиту или по случайному заданному в настройках: reddit art"""
    interesting_subreddit = raw_subreddit
    if not interesting_subreddit:
        interesting_subreddit = random.choice(settings.REPOS.REDDIT.SUBS) if settings.REPOS.REDDIT.SUBS else DEFAULT_SUBREDDIT

    reddit_post_info = reddit_repository.get_random_latest_post_by_subreddit(interesting_subreddit)
    if not reddit_post_info:
        return ResultCommandText("Не удалось извлечь пост из reddit")
    post_url, post_title, picture_url = reddit_repository.get_random_latest_post_by_subreddit(interesting_subreddit)
    post_text = f"[{interesting_subreddit}] {post_title} {post_url}"
    return ResultCommandTextPicture(post_text, picture_url) if picture_url else ResultCommandText(post_text)
