"""Репозиторий запросов к bash.im"""

from requests_html import HTMLSession


class BashimRepository:

    def get_random_quote(self) -> str:
        """Вернет случайную цитату."""
        session = HTMLSession()
        request = session.get("https://bash.im/random")
        element_quote = request.html.find(".quote .quote__body", first=True)
        if element_quote:
            return element_quote.text
        return ""
