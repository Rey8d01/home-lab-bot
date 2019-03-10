"""Общие команды."""

from . import register_command, COMMANDS, ResultCommandText


@register_command
def _hello() -> ResultCommandText:
    """Вернет 'Hello world!'."""
    return ResultCommandText("Hello world!")


@register_command
def _ping() -> ResultCommandText:
    """Если бот работает, вернет 'Pong!'."""
    return ResultCommandText("Pong!")


@register_command
def _help() -> ResultCommandText:
    """Покажет эту справку по коммандам."""
    return ResultCommandText(
        "\n".join((f"{name_command} - {fn_command.__doc__}" for name_command, fn_command in COMMANDS.items()))
    )
