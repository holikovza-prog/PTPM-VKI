"""Класс взаимодействия с пользователем. Абстрактный базовый класс — интерфейс."""

import logging
from abc import ABC, abstractmethod


class UserInterface(ABC):
    """Интерфейс получения данных от пользователя."""

    @abstractmethod
    def get_sides(self):
        """Возвращает три строки со сторонами треугольника."""


class ConsoleUserInterface(UserInterface):
    """Реализация интерфейса: читает три строки через input()."""

    PROMPTS = (
        "Введите длину стороны A: ",
        "Введите длину стороны B: ",
        "Введите длину стороны C: ",
    )

    def get_sides(self):
        """Читает три строки. При прерывании ввода подставляет пустую строку."""
        sides = []
        for index, prompt in enumerate(self.PROMPTS, start=1):
            try:
                sides.append(input(prompt))
            except EOFError:
                logging.warning("Ввод прерван на стороне %s", index)
                sides.append("")
        logging.debug("Получены стороны: %s", sides)
        return sides