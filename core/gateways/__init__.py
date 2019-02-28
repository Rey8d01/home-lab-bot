"""Модуль с перечнем доступных платформ для работы бота.

Каждая реализация доступа к платформе должна реализовать функцию talk,
запуск которой приведет к работе бота в этой среде.

"""

import importlib

from core.exceptions import UndefinedGateway


def adapter(settings):
    """Запускает интерфейс общения с чатом в gateway."""
    gateway = settings["geth"]["default_im"]
    settings_im = settings["im"].get(gateway)
    if settings_im is None:
        raise UndefinedGateway(f"Settings not contain section [im.{gateway}]")
    try:
        module_gateway = importlib.import_module(f"core.gateways.{gateway}")
    except ModuleNotFoundError:
        raise UndefinedGateway(f"Settings for {gateway} found, but module does not exists")
    module_gateway.Gateway(**settings_im).talk()
