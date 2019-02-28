"""Процесс подключения и сборки файлов конфигурации.

Формат файлов конфигурации принят как TOML.

Демо пример конфига есть в файле settings/defaults.toml
альтернативные файлы конфигурации можно размещать в той же директории
(содержимое игнорируется правилами .gitignore) и задавать их имя при запуске через переменную окружения,
имя которой определяется здесь константой ENV_KEY_SETTINGS.
При запуске настройки будут рекурсивно объединены с дефолтными и перекрыты кастомными.

"""

import os
import typing
from pathlib import Path

import anyconfig

from core.exceptions import ReadSettingsException

BASE_PATH = Path()
SETTINGS_PATH = BASE_PATH / "settings"
DEFAULT_SETTINGS_FILENAME = "defaults"
ENV_KEY_SETTINGS = "GETH_SETTINGS"


class Config:
    """Класс с настройками (Borg)."""
    __shared_state = {}

    def __init__(self):
        """В случае пустых настроек - задается начальное состояние из файлов настроек.

        Актуально при первой загрузке.

        """
        self.__dict__ = self.__shared_state
        if not self.__shared_state:
            self.paths_settings = ()
            self.settings = {}
            self.load()

    def load(self):
        """Считывание настроек из файлов и загрузка их в состояние класса настроек."""
        self.paths_settings = tuple(filter(None, (self._path_default_settings(), self._path_local_settings())))
        self.settings = anyconfig.load(self.paths_settings)

    def _path_default_settings(self) -> str:
        """Подключение дефолтной конфигурации."""
        path_default_settings = (SETTINGS_PATH / DEFAULT_SETTINGS_FILENAME).with_suffix(".toml")
        if not path_default_settings.is_file():
            raise ReadSettingsException(f"Default config not found (default path '{path_default_settings}')")
        return str(path_default_settings.resolve())

    def _path_local_settings(self) -> typing.Optional[str]:
        """Подключение локальной конфигурации."""
        filename_local_settings = os.environ.get(ENV_KEY_SETTINGS)
        if filename_local_settings:
            path_local_settings = (SETTINGS_PATH / filename_local_settings).with_suffix(".toml")
            if path_local_settings.is_file():
                return str(path_local_settings.resolve())
        return None
