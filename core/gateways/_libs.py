"""Библиотечные функции и классы для работы интерфейсов."""


class GatewayInterface:
    """Интерфейс для платформ с которых предполагается взаимодействие с ботом."""

    def talk(self):
        """Основной метод для запуска общения.

        Должен реализовать подключение к платформе и реагировать на поступающие сообщения.

        """
        raise NotImplementedError("Method 'talk' must be implemented.")
