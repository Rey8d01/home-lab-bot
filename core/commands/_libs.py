"""Библиотечные функции, базовые классы модуля и его интерфейсы."""
from dataclasses import dataclass


class ResultCommand:
    """Интерфейсный класс для результатов выполнения команд."""
    pass


@dataclass
class ResultCommandText(ResultCommand):
    """Результат выполнения команды с текстом."""
    text: str


@dataclass
class ResultCommandTextPicture(ResultCommand):
    """Результат выполнения команды с текстом и URL до картинки."""
    text: str
    picture_url: str