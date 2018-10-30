"""Процесс подключения и сборки файлов конфигурации."""

import os
from pathlib import Path

import collections

import toml

from core.exceptions import ReadSettingsException

BASE_PATH = Path()
ENV_KEY_SETTINGS = "GETH_SETTINGS"


def read_default_settings():
    """Подключение дефолтной конфигурации."""
    path_file_default_settings = (BASE_PATH / "settings" / "defaults.toml").with_suffix(".toml")
    if not path_file_default_settings.is_file():
        raise ReadSettingsException(f"Default config not found (default path '{path_file_default_settings}')")
    return toml.load(path_file_default_settings)


def read_local_settings():
    """Подключение локальной конфигурации."""
    local_settings = {}
    filename_local_settings = os.environ.get(ENV_KEY_SETTINGS)
    if filename_local_settings:
        path_file_local_settings = (BASE_PATH / "settings" / filename_local_settings).with_suffix(".toml")
        if path_file_local_settings.is_file():
            local_settings = toml.load(path_file_local_settings)
    return local_settings


def merge_dict(d1, d2):
    """
    Modifies d1 in-place to contain values from d2.  If any value
    in d1 is a dictionary (or dict-like), *and* the corresponding
    value in d2 is also a dictionary, then merge them in-place.
    """
    for k, v2 in d2.items():
        v1 = d1.get(k)  # returns None if v1 has no value for this key
        if isinstance(v1, collections.Mapping) and isinstance(v2, collections.Mapping):
            merge_dict(v1, v2)
        else:
            d1[k] = v2


settings = {}
merge_dict(settings, read_default_settings())
merge_dict(settings, read_local_settings())
