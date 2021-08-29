"""Описания исключений для приложения."""


class CoreException(Exception):
    pass


class ReadSettingsException(CoreException):
    pass


class UndefinedGateway(CoreException):
    pass


class CommandException(CoreException):
    pass


class UndefinedCommand(CommandException):
    pass


class ErrorCommand(CommandException):
    pass


class CoreWarning(UserWarning):
    pass
