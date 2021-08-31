"""Сборка и настройка параметров рабочего окружения.

Формат файлов конфигурации принят как TOML.

Демо пример конфига есть в файле config/settings.toml
альтернативные файлы конфигурации можно размещать в той же директории
и их подключение регулируется библиотекой dynaconf.

"""

import logging
from pathlib import Path

from dynaconf import Dynaconf

settings = Dynaconf(
    environments=True,
    envvar_prefix="HLB",  # `envvar_prefix` = export envvars with `export HLB_FOO=bar`.
    settings_files=("settings.toml", "local_settings.toml"),  # Порядок загрузки файлов - последние перекрывают предыдущие.
    MERGE_ENABLED_FOR_DYNACONF=True,
)

# Настройка директории для хранения временных файлов и прочего локального барахла.
LOCAL_TMP_PATH = Path() / "tmp"
LOCAL_TMP_PATH.mkdir(mode=0o755, exist_ok=True)

# Logging
_log_level = logging.DEBUG if settings.DEBUG else logging.WARNING
logging.basicConfig(
    format="%(levelname)s %(asctime)s %(name)s %(message)s",
    filename=LOCAL_TMP_PATH / "hlb.log",
    encoding="utf-8",
    level=_log_level
)
logger = logging.getLogger(__name__)

logger.info("Settings and logger are loaded")
