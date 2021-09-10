"""Основной скрипт для запуска бота.

Экземпляр бота запускается на конкретной платформе - месте где происходит взаимодействие с ботом.
Выбор платформы определяется через настройки, а запуск работы с ней происходит через адаптер в модуле `core.gateways`

"""

import logging

from core.gateways.start_talk import start_talk
from core.services.signals import setup_signal_handlers

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Start bot")

    setup_signal_handlers()
    try:
        start_talk()
    except SystemExit:
        # todo shutdown
        pass
