"""Основной программный API."""

from .repositories.bashim import BashimRepository


def get_random_quote_bashim():
    return BashimRepository().get_random_quote()
