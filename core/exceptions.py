"""Описания исключений для приложения."""


class CoreException(Exception):
    pass


class ReadSettingsException(CoreException):
    pass


class UndefinedCommand(CoreException):
    pass


class CoreWarning(UserWarning):
    pass
