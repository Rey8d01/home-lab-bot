"""Подключение к выбранному модулю с интеграцией с платформой."""

import importlib
import logging

from config import settings
from core.exceptions import UndefinedGateway

logger = logging.getLogger(__name__)


def start_talk():
    """Основной фасадный метод для запуска процесса общения в чате через заданный gateway."""
    gateway = settings.DEFAULT_IM
    im_settings = settings.IM.get(gateway)
    if im_settings is None:
        raise UndefinedGateway(f"Settings not contain section [im.{gateway}]")
    try:
        module_gateway = importlib.import_module(f"core.gateways.libs.{gateway}")
    except ModuleNotFoundError:
        raise UndefinedGateway(f"Settings for {gateway} found, but module does not exists")
    logger.debug(f"Connect to gateway {gateway!r} with settings: {im_settings!r}")
    module_gateway.Gateway(im_settings).talk()
