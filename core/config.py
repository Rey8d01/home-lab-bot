"""Процесс подключения и сборки файлов конфигурации."""

import os
import typing
from pathlib import Path

import anyconfig

from core.exceptions import ReadSettingsException

BASE_PATH = Path()
SETTINGS_PATH = BASE_PATH / "settings"
ENV_KEY_SETTINGS = "GETH_SETTINGS"


def _path_default_settings() -> str:
    """Подключение дефолтной конфигурации."""
    path_default_settings = (SETTINGS_PATH / "defaults.toml").with_suffix(".toml")
    if not path_default_settings.is_file():
        raise ReadSettingsException(f"Default config not found (default path '{path_default_settings}')")
    return str(path_default_settings.resolve())


def _path_local_settings() -> typing.Optional[str]:
    """Подключение локальной конфигурации."""
    filename_local_settings = os.environ.get(ENV_KEY_SETTINGS)
    if filename_local_settings:
        path_local_settings = (SETTINGS_PATH / filename_local_settings).with_suffix(".toml")
        if path_local_settings.is_file():
            return str(path_local_settings.resolve())
    return None


_paths_settings = tuple(filter(None, (_path_default_settings(), _path_local_settings())))
settings = anyconfig.load(_paths_settings)
