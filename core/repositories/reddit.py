"""Репозиторий запросов к reddit.com"""

import random
from typing import Optional, Tuple

import praw

from config import settings


class RedditRepository:

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=settings.REPOS.REDDIT.CLIENT_ID,
            client_secret=settings.REPOS.REDDIT.CLIENT_SECRET,
            user_agent=settings.TITLE
        )

    def get_random_latest_post_by_subreddit(self, subreddit: str) -> Optional[Tuple[str, str, Optional[str]]]:
        """Вернет информацию по какому-нибудь последнему посту из заданного сабреддита.

        Если не возникло проблем с получением поста то будет возвращен кортеж из 3х элементов:
            - URL поста;
            - заголовок поста;
            - URL картинки или поста.

        """
        # Пролистываем случайное количество постов.
        submission = None
        for submission in self.reddit.subreddit(subreddit).new(limit=random.randint(1, 11)):
            pass
        if not submission:
            return None

        picture_url = None
        if hasattr(submission, "post_hint") and submission.post_hint == "image":
            picture_url = submission.url
        return submission.shortlink, submission.title, picture_url
