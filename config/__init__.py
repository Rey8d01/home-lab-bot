"""Сборка и настройка параметров рабочего окружения.

Формат файлов конфигурации принят как TOML.

Демо пример конфига есть в файле config/settings.toml
альтернативные файлы конфигурации можно размещать в той же директории
и их подключение регулируется библиотекой dynaconf.

"""

import logging

from dynaconf import LazySettings

# Settings
settings = LazySettings(
    SETTINGS_MODULE="config/settings.toml",
    MERGE_ENABLED_FOR_DYNACONF=True,
    GLOBAL_ENV_FOR_DYNACONF="GETH"
)

# Logging
_log_level = logging.DEBUG if settings.DEBUG else logging.WARNING
logging.basicConfig(level=_log_level)
logger = logging.getLogger(__name__)

logger.debug("Settings and logger are loaded")
