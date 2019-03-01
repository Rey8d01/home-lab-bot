"""Общие команды."""

from . import register_command, COMMANDS


@register_command
def _hello() -> str:
    """Вернет 'Hello world!'."""
    return "Hello world!"


@register_command
def _ping() -> str:
    """Если бот работает, вернет 'Pong!'."""
    return "Pong!"


@register_command
def _help() -> str:
    """Покажет эту справку по коммандам."""
    return "\n".join((f"{name_command} - {fn_command.__doc__}" for name_command, fn_command in COMMANDS.items()))
