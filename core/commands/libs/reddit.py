"""Команды для использования reddit."""

import random

from config import settings
from core.commands.interfaces import TextCommandResult, TextWithPictureCommandResult, CommandResult
from core.commands.utils import register_command
from core.repositories.reddit import RedditRepository

DEFAULT_SUBREDDIT = "all"  # Если интересные сабреддиты в конфиге не указаны, будет использован этот.
reddit_repository = RedditRepository()


@register_command(aliases=("r", "reddit", "р", "реддит"))
def reddit(raw_subreddit: str, **kwargs) -> CommandResult:
    """Покажет случайный пост по указанному сабреддиту или по случайному заданному в настройках: reddit art"""
    interesting_subreddit = raw_subreddit
    if not interesting_subreddit:
        interesting_subreddit = random.choice(settings.REPOS.REDDIT.SUBS) if settings.REPOS.REDDIT.SUBS else DEFAULT_SUBREDDIT

    reddit_post_info = reddit_repository.get_random_latest_post_by_subreddit(interesting_subreddit)
    if not reddit_post_info:
        return TextCommandResult("Не удалось извлечь пост из reddit")
    post_url, post_title, picture_url = reddit_post_info
    post_text = f"[{interesting_subreddit}] {post_title} {post_url}"
    return TextWithPictureCommandResult(post_text, picture_url) if picture_url else TextCommandResult(post_text)
