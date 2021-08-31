"""Основной программный API.

Все команды публикуются в текущем модуле и будут динамически подгружаться (без явного импорта).

Каждая функция команды должна быть задекорирована через register_command,
все правила и разрешения будут реализовываться через нее.
Сигнатура функции команды должна иметь как минимум (*args, **kwargs) для игнорирования случайно переданных лишних аргументов.
В общем случае все что идет после названия команды будет передано функцию в сыром виде, т.е. как строка.

Функция команды должна возвращать результат в виде объекта класса-результата, которые объявлены ниже.
Это нужно чтобы стандартизировать ответ,
а каждая платформа сама сможет его интерпретировать и отправлять результат в нужном для нее виде.

"""

import time
import logging
from dataclasses import dataclass
from importlib import import_module
from importlib import resources

from core.exceptions import UndefinedCommand, CoreWarning, ErrorCommand

logger = logging.getLogger(__name__)
COMMANDS = {}  # Список зарегистрированных команд для вызова.
PRIVATE_COMMANDS = []  # Список приватных команд, к которым ограничен доступ.
HELPERS_FOR_COMMANDS = {}  # Перечень мануалов для команд.


@dataclass
class ResultCommandText:
    """Результат выполнения команды с текстом."""
    text: str


@dataclass
class ResultCommandTextPicture:
    """Результат выполнения команды с текстом и URL до картинки."""
    text: str
    picture_url: str


def _process_register_command(func, aliases: tuple, is_private: bool):
    """Процесс сохранения зарегистрированных команд.

    Проверяется наличие команд с одинаковыми алиасами, под которыми можно запустить команду.
    Генерируется описания команд для команды `help`.
    Если был передан флаг `is_private = True`, то эта отметка сохраняется чтобы только специальные пользователи могли вызвать команду.

    """
    if not aliases:
        # Если алиасов не было указано, используется собственное имя функции для команды.
        alias: str = func.__name__
        aliases = (alias,)

    wrong_commands = set(COMMANDS).intersection(aliases)
    if wrong_commands:
        raise CoreWarning(f"Commands {wrong_commands!r} are not unique")

    COMMANDS.update({alias: func for alias in aliases})
    is_private and PRIVATE_COMMANDS.extend(aliases)

    first_alias = aliases[0]
    other_aliases = f" ({' '.join(aliases[1:])})" if aliases[1:] else ""
    HELPERS_FOR_COMMANDS[first_alias] = f"{first_alias}{other_aliases} - {func.__doc__}"

    return func


def register_command(func=None, aliases: tuple = (), is_private: bool = False):
    """Декоратор для регистрации функций команд.

    Можно декоратор использовать через вызов @register_command(), так и без @register_command.
    Но лучше с вызовом чтобы передавать нормальный список алиасов для вызова функции.

    """

    def wrap(_func):
        return _process_register_command(_func, aliases, is_private)

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


def handle_command(raw_command: str, is_super_user: bool = False) -> str:
    """Общая обработка переданной команды и ее непосредственный вызов.

    Если команда объявлена приватной (специальной), а флаг `is_super_user = False`, то обработка не наступит.

    """
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

    if command_name in PRIVATE_COMMANDS and not is_super_user:
        logger.warning(f"Call private command {command_name!r} for non super user")
        raise UndefinedCommand() from None

    logger.debug(f"Call command {command_name!r}")
    command_start_time = time.time()
    try:
        result_command = fn_command(command_args, is_super_user=is_super_user)
    except Exception as error:
        logger.error("Error while executing command", exc_info=error)
        raise ErrorCommand() from None

    command_delta = int((time.time() - command_start_time) * 1000)
    logger.debug(f"Call command {command_name!r} ended in {command_delta} ms")

    return result_command
