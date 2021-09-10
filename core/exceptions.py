"""Описания исключений для приложения."""


class CoreException(Exception):
    """Общее исключение. Требует наследования, для уточнения ситуации."""


class UndefinedGateway(CoreException):
    """Исключение для ситуаций с ошибками определения платформы для работы бота."""


class CommandException(CoreException):
    """Общее исключение для ошибок при выполнении команд."""


class UndefinedCommand(CommandException):
    """Ошибка определения команды."""


class ErrorCommand(CommandException):
    """Ошибка выполнения команды."""


class CoreWarning(UserWarning):
    """Общее предупреждение. Требует наследования, для уточнения ситуации."""
