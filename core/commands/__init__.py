"""Модуль для регистрации и обработки команд."""
import logging
import time
from importlib import import_module, resources
from typing import Dict, Callable, List

from core.commands._libs import CommandResult
from core.exceptions import UndefinedCommand, ErrorCommand, CommandException

logger = logging.getLogger(__name__)
COMMANDS: Dict[str, Callable[..., CommandResult]] = {}  # Список зарегистрированных команд для вызова.
PRIVATE_COMMANDS: List[str] = []  # Список приватных команд, к которым ограничен доступ.
HELPERS_FOR_COMMANDS: Dict[str, str] = {}  # Перечень мануалов для команд.


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
        raise CommandException(f"Commands {wrong_commands!r} are not unique")

    COMMANDS.update({alias: func for alias in aliases})
    is_private and PRIVATE_COMMANDS.extend(aliases)  # type: ignore[func-returns-value]

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


def handle_command(raw_command: str, is_super_user: bool = False) -> CommandResult:
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
        command_function = COMMANDS[command_name]
    except KeyError:
        _import_commands()
        command_function = COMMANDS.get(command_name)
        if command_function is None:
            logger.warning(f"Call undefined command {command_name!r}")
            raise UndefinedCommand() from None

    if command_name in PRIVATE_COMMANDS and not is_super_user:
        logger.warning(f"Call private command {command_name!r} for non super user")
        raise UndefinedCommand() from None

    logger.debug(f"Call command {command_name!r}")
    command_start_time = time.time()
    try:
        command_result = command_function(command_args, is_super_user=is_super_user)
    except Exception as error:
        logger.error("Error while executing command", exc_info=error)
        raise ErrorCommand() from None

    command_delta = int((time.time() - command_start_time) * 1000)
    logger.debug(f"Call command {command_name!r} ended in {command_delta} ms")

    return command_result
