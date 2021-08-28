"""Основной программный API.

Все команды публикуются в текущем модуле и будут динамически подгружаться (без явного импорта).

Функция команды должна быть задекорирована через register_command,
все правила и разрешения будут реализовываться через нее.

Сигнатуры функций команд должны иметь как минимум (*args) для игнорирования случайно переданных лишних аргументов.

Функция команды должна возвращать результат в виде объекта класса-результата, которые объявлены ниже.
Это нужно чтобы стандартизировать ответ,
а каждая платформа сама сможет его интерпретировать и отправлять результат в нужном для нее виде.

"""

import time
import logging
from dataclasses import dataclass
from importlib import import_module
from importlib import resources

from core.exceptions import UndefinedCommand, CoreWarning

logger = logging.getLogger(__name__)
COMMANDS = {}  # Список зарегистрированных команд для вызова.
HELPERS_FOR_COMMANDS = {}  # Перечень мануалов для команд.


@dataclass
class ResultCommandText:
    """Результат выполнения команды с текстом."""
    text: str


@dataclass
class ResultCommandTextPicture:
    """Результат выполнения команды с текстом и URL до картинки."""
    text: str
    url_picture: str


def _process_register_command(func, aliases: tuple):
    """Процесс сохранения зарегистрированных команд.

    Проверяется наличие команд с одинаковыми именами.
    Генерируется описания команд для команды `help`.

    """
    if not aliases:
        # Если алиасов не было указано, используется собственное имя функции для команды.
        alias: str = func.__name__
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


def register_command(func=None, aliases: tuple = ()):
    """Декоратор для регистрации функций команд.

    Можно декоратор использовать через вызов @register_command(), так и без @register_command.
    Но лучше с вызовом чтобы передавать нормальный список алиасов для вызова функции.

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
    """Обработка команд."""
    command_parts = raw_command.split(maxsplit=1)
    command_name = command_parts[0]
    command_args = ""
    if len(command_parts) > 1:
        command_args = command_parts[1]

    # Если команда не была найдена при первом обращении, происходит импорт всех команд и повторный ее вызов.
    try:
        fn_command = COMMANDS[command_name]
    except KeyError:
        _import_commands()
        if command_name in COMMANDS:
            fn_command = COMMANDS[command_name]
        else:
            logger.warning(f"Call undefined command {command_name!r}")
            raise UndefinedCommand() from None

    logger.debug(f"Call command {command_name!r}")
    command_start_time = time.time()
    result_command = fn_command(command_args)
    command_delta = int((time.time() - command_start_time) * 1000)
    logger.debug(f"Call command {command_name!r} ended in {command_delta} ms")

    return result_command
