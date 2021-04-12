"""Модуль с перечнем доступных платформ, на которых может работать бот.

Чтобы бот начал работать на какой-то платформе, у него должна быть реализация с доступом к ней.
Каждая реализация доступа к платформе представлена в виде файла или модуля, имя которого будет являться ключом в настройках запуска.

Внутри класса или модуля доступа к платформе должен быть класс с именем `Gateway`,
который реализует интерфейс `core.gateways._libs.GatewayInterface`.

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
