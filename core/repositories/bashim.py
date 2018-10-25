"""Репозиторий запросов к bash.im"""
from requests_html import HTMLSession

__all__ = ("BashimRepository",)


class BashimRepository:

    def __init__(self):
        pass

    def get_random_quote(self) -> str:
        """Вернет случайную цитату."""
        session = HTMLSession()
        request = session.get("https://bash.im/random")
        element_quote = request.html.find(".quote .text", first=True)
        if element_quote:
            return element_quote.text
        return ""
