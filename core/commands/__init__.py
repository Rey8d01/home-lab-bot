"""Основной программный API.

Все команды публикуются в текущем модуле и будут динамически подгружатся (без явного импорта).

Правила публикации команды:

    - имя функции команды используется для ее вызова через интерфейс, поэтому оно должно быть удобным;
    - имя функции команды должно начинатся с _ (нижнее подчеркивание) для того,
    чтобы была возможность безопасно использовать имена зарезервированных функций, при регистрации символ будет удален;
    - функция команды должна быть задекорирована через register_command;

"""

import logging
from dataclasses import dataclass
from importlib import import_module
from importlib import resources

from core.exceptions import UndefinedCommand, CoreWarning

logger = logging.getLogger(__name__)
COMMANDS = {}


@dataclass
class ResultCommandText:
    """Результат выполнения команды с текстом."""
    text: str


@dataclass
class ResultCommandTextPicture:
    """Результат выполнения команды с текстом и URL до картинки."""
    text: str
    url_picture: str


def register_command(func):
    """Декоратор для регистрации функций команд.

    Срезается _ у команды чтобы была возможность использовать ее нормальное имя.
    Проверяется наличие команд с одинаковыми именами.

    """
    name: str = func.__name__
    if name.startswith("_"):
        name = name[1:]
    if name in COMMANDS:
        raise CoreWarning(f"Command {func.__name__!r} is not unique")
    COMMANDS[name] = func
    return func


def __dir__():
    """Список доступных команд."""
    _import_commands()
    return list(COMMANDS.keys())


def _import_commands():
    """Импортирует все ресурсы для регистрации команд.

    Поиск и импорт всех .py файлов в текущем модуле, кроме текущего __init__.py

    """
    for name in resources.contents(__name__):
        if name.endswith(".py") and not name == "__init__.py":
            logger.debug(f"Import module of commands {name!r}")
            import_module(f"{__name__}.{name[:-3]}")


def handle_command(raw_command: str) -> str:
    """Обработка комманд.

    Если команда не была найдена при первом обращении, происходит импорт всех команд и повторный ее вызов.

    """
    parts_command = raw_command.split(maxsplit=1)
    name_command = parts_command[0]
    args_command = ""
    if len(parts_command) > 1:
        args_command = parts_command[1]

    try:
        fn_command = COMMANDS[name_command]
    except KeyError:
        _import_commands()
        if name_command in COMMANDS:
            fn_command = COMMANDS[name_command]
        else:
            logger.warning(f"Call undefined command {name_command!r}")
            raise UndefinedCommand() from None

    logger.debug(f"Call command {name_command!r}")
    return fn_command(args_command)
