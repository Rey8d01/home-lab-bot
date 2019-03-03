"""Модуль с перечнем доступных платформ для работы бота.

Каждая реализация доступа к платформе должна реализовать функцию talk,
запуск которой приведет к работе бота в этой среде.

"""

import importlib
import logging

from config import settings
from core.exceptions import UndefinedGateway

logger = logging.getLogger(__name__)


def adapter():
    """Запускает интерфейс общения с чатом в gateway."""
    gateway = settings.DEFAULT_IM
    settings_im = settings.IM.get(gateway)
    if settings_im is None:
        raise UndefinedGateway(f"Settings not contain section [im.{gateway}]")
    try:
        module_gateway = importlib.import_module(f"core.gateways.{gateway}")
    except ModuleNotFoundError:
        raise UndefinedGateway(f"Settings for {gateway} found, but module does not exists")
    logger.debug(f"Connect to gateway {gateway!r} with settings: {settings_im!r}")
    module_gateway.Gateway(settings_im).talk()
