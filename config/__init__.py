"""Сборка и настройка параметров рабочего окружения.

Формат файлов конфигурации принят как TOML.

Демо пример конфига есть в файле config/settings.toml
альтернативные файлы конфигурации можно размещать в той же директории
и их подключение регулируется библиотекой dynaconf.

"""

import logging

from dynaconf import Dynaconf

settings = Dynaconf(
    environments=True,
    envvar_prefix="GETH",  # `envvar_prefix` = export envvars with `export GETH_FOO=bar`.
    settings_files=("settings.toml", "local_settings.toml"),  # Порядок загрузки файлов - последние перекрывают предыдущие.
    MERGE_ENABLED_FOR_DYNACONF=True,
)

# Logging
_log_level = logging.DEBUG if settings.DEBUG else logging.WARNING
logging.basicConfig(level=_log_level)
logger = logging.getLogger(__name__)

logger.debug("Settings and logger are loaded")
