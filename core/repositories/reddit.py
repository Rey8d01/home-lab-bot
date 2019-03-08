"""Репозиторий запросов к reddit.com"""

import random

import praw

from config import settings


class RedditRepository:

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=settings.REPOS.REDDIT.CLIENT_ID,
            client_secret=settings.REPOS.REDDIT.CLIENT_SECRET,
            user_agent=settings.TITLE
        )

    def get_random_post(self):
        name_random_subreddit = random.choice(settings.REPOS.REDDIT.SUBS)
        if not name_random_subreddit:
            return ""

        submission = self.reddit.subreddit(name_random_subreddit).random()
        return f"{submission.title} {submission.url}"
