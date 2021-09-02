"""Тестирование функций ядра системы."""
from config import settings


def test_settings():
    """Простой тест для базовых настроек."""
    gateway = settings.DEFAULT_IM
    assert gateway == "cli"
