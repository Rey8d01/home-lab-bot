"""Репозиторий запросов к bash.im"""
from typing import Optional

from requests_html import HTMLSession


def get_random_quote() -> Optional[str]:
    """Вернет случайную цитату."""
    session = HTMLSession()
    request = session.get("https://bash.im/random")
    element_quote = request.html.find(".quote .quote__body", first=True)
    if element_quote:
        return element_quote.text
    return None
