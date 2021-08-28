"""Обработка Unix signals."""

import signal
import logging

logger = logging.getLogger(__name__)


def setup_signal_handlers():
    """Общая функция регистрации обработчиков сигналов. Вызывать при запуске приложения."""
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGUSR1, ping)


def shutdown(sig, stack):
    """Обработка сигнала для завершения работы программы."""
    logger.info("Shutdown bot")
    raise SystemExit()


def ping(sig, stack):
    """Обработка пользовательского сигнала. Как пример пинг - просто запись в лог"""
    logger.info("Ping bot")
