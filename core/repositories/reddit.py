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

    def get_random_latest_post(self) -> Optional[Tuple[str, str, str, Optional[str]]]:
        """Вернет информацию по какому-нибудь последнему посту из заданных подписок.

        Если не возникло проблем с получением поста то будет возвращен кортеж из 3х элементов:
            - название сабреддита;
            - URL поста;
            - заголовок поста;
            - URL картинки или поста.

        """
        name_random_subreddit = random.choice(settings.REPOS.REDDIT.SUBS)
        if not name_random_subreddit:
            return None

        # Пролистываем случайное количество постов.
        submission = None
        for submission in self.reddit.subreddit(name_random_subreddit).new(limit=random.randint(1, 11)):
            pass
        if not submission:
            return None

        url_picture = None
        if hasattr(submission, "post_hint") and submission.post_hint == "image":
            url_picture = submission.url
        return name_random_subreddit, submission.shortlink, submission.title, url_picture
