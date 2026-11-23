"""Класс сторонней зависимости. Абстрактный базовый класс — интерфейс."""

import logging
from abc import ABC, abstractmethod


class ExternalService(ABC):
    """Интерфейс отправки результата стороннему процессу."""

    @abstractmethod
    def send(self, message):
        """Отправляет строку-результат. Возвращает True при успехе."""


class NotificationService(ExternalService):
    """Имитация отправки данных: складывает сообщения в список и пишет в лог.

    Реальная отправка не выполняется — это заглушка внешнего сервиса.
    """

    def __init__(self):
        self.sent = []

    def send(self, message):
        self.sent.append(message)
        logging.info("Отправлено внешнему сервису: %s", message)
        return True