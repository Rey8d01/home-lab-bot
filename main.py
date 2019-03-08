"""Запуск бота."""

from core.gateways import adapter
import logging

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Start bot")
    adapter()
