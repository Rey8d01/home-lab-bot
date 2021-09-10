"""Базовые классы модуля и его интерфейсы."""

from dataclasses import dataclass


class CommandResult:
    """Интерфейсный класс для результатов выполнения команд."""


@dataclass
class TextCommandResult(CommandResult):
    """Результат выполнения команды с текстом."""
    text: str


@dataclass
class TextWithPictureCommandResult(CommandResult):
    """Результат выполнения команды с текстом и URL до картинки."""
    text: str
    picture_url: str
