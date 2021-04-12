"""Основной скрипт для запуска бота.

Экземпляр бота запускается на конкретной платформе - месте где происходит взаимодействие с ботом.
Выбор платформы определяется через настройки, а запуск работы с ней происходит через адаптер в модуле `core.gateways`

"""

from core.gateways import adapter
import logging

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Start bot")
    adapter()
