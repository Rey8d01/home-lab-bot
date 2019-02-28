"""Запуск бота."""

from core.config import Config
from core.gateways import adapter


if __name__ == "__main__":
    adapter(Config().settings)
