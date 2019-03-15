"""Основной программный API.

Все команды публикуются в текущем модуле и будут динамически подгружатся (без явного импорта).

Функция команды должна быть задекорирована через register_command,
все правила и разрешения будут реализовываться через нее.

Функция команды должна возвращать результат в виде объекта класса-результата, которые объявлены ниже.
Это нужно чтобы стандартизировать ответ,
а каждая платформа сама сможет его интерпретировать и отправлять результат в нужном для нее виде.

"""

import logging
from dataclasses import dataclass
from importlib import import_module
from importlib import resources

from core.exceptions import UndefinedCommand, CoreWarning

logger = logging.getLogger(__name__)
COMMANDS = {}
HELPERS_FOR_COMMANDS = {}


@dataclass
class ResultCommandText:
    """Результат выполнения команды с текстом."""
    text: str


@dataclass
class ResultCommandTextPicture:
    """Результат выполнения команды с текстом и URL до картинки."""
    text: str
    url_picture: str


def _process_register_command(func, aliases: list):
    """Процесс сохранения зарегистрированных комманд.

    В случае дефолтного варианта (без списка вызываемых коммнд для функции) с
    резается _ у имя функции чтобы была возможность использовать ее имя.

    Проверяется наличие команд с одинаковыми именами.

    Генерируется описания команд для _help фнукции.

    """
    if not aliases:
        alias: str = func.__name__
        if alias.startswith("_"):
            alias = alias[1:]
        aliases = (alias,)

    wrong_commands = set(COMMANDS).intersection(aliases)
    if wrong_commands:
        raise CoreWarning(f"Commands {wrong_commands!r} are not unique")

    for alias in aliases:
        COMMANDS[alias] = func

    first_alias = aliases[0]
    other_aliases = f" ({' '.join(aliases[1:])})" if aliases[1:] else ""
    HELPERS_FOR_COMMANDS[first_alias] = f"{first_alias}{other_aliases} - {func.__doc__}"

    return func


def register_command(func=None, aliases: list = ()):
    """Декоратор для регистрации функций команд.

    Можно декоратор использовать через вызов @register_command(), так и без @register_command.
    Но лучше с вызовом чтобы передавать нормальный список команд для вызова функции.

    """

    def wrap(_func):
        return _process_register_command(_func, aliases)

    if func is None:
        return wrap
    return wrap(func)


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
