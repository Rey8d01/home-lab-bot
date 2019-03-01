"""Запуск бота."""

from core.config import Config
from core.gateways import adapter


if __name__ == "__main__":
    config = Config()
    config.logger.info("Start bot")
    adapter(config)

