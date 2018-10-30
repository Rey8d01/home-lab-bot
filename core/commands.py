"""Основной программный API."""

from core.repositories.bashim import BashimRepository
from core.exceptions import UndefinedCommand


def _hello() -> str:
    """Вернет 'Hello world!'."""
    return "Hello world!"


def _ping() -> str:
    """Если бот работает, вернет 'Pong!'."""
    return "Pong!"


def _help() -> str:
    """Покажет эту справку по коммандам."""
    return "\n".join((f"{name_command} - {fn_command.__doc__}" for name_command, fn_command in commands.items()))


def _get_random_quote_bashim() -> str:
    """Покажет случайную цитату с bash.im"""
    return BashimRepository().get_random_quote()


commands = {
    "/hello": _hello,
    "/ping": _ping,
    "/help": _help,
    "/bash": _get_random_quote_bashim,
}


def handle_command(command: str) -> str:
    """Обработка комманд."""
    fn_command = commands.get(command)

    if fn_command is None:
        raise UndefinedCommand()

    return fn_command()
