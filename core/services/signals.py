"""Обработка Unix signals."""

import signal
import logging

logger = logging.getLogger(__name__)


def shutdown(sig, stack):
    logger.info("Shutdown bot")
    raise SystemExit()


def setup_signal_handlers():
    """Общая функция регистрации обработчиков сигналов. Вызывать при запуске приложения."""
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
