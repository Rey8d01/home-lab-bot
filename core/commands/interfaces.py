"""Базовые классы модуля и его интерфейсы."""

from dataclasses import dataclass
from typing import BinaryIO, Optional


class CommandResult:
    """Интерфейсный класс для результатов выполнения команд."""


@dataclass
class TextCommandResult(CommandResult):
    """Результат выполнения команды с текстом."""
    text: str


@dataclass
class TextWithPictureURLCommandResult(CommandResult):
    """Результат выполнения команды с текстом и URL до картинки."""
    text: str
    picture_url: str


@dataclass
class TextWithPictureFileCommandResult(CommandResult):
    """Результат выполнения команды с текстом и файлом с картинкой.

    Картинку нужно передать в двух вариантах: байтовый и строковый. Чтобы платформа сама решила как ей поступить с этим типом.

    """
    text: str
    picture_as_bytes: BinaryIO
    picture_as_str: Optional[str]
