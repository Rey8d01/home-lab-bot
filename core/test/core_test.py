from config import settings


def test_settings():
    gateway = settings.DEFAULT_IM
    assert gateway == "cli"
