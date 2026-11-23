"""Класс-контроллер: связывает вычисления, БД, ввод и внешний сервис."""

import logging


class Controller:
    """Сквозной сценарий: спросить данные, посчитать, сохранить, отправить."""

    def __init__(self, calculator, repository, user_interface, external_service):
        self.calculator = calculator
        self.repository = repository
        self.user_interface = user_interface
        self.external_service = external_service

    def run(self):
        """Выполняет сценарий и возвращает (тип, координаты, текст ошибки, источник)."""
        sides = self.user_interface.get_sides()
        triangle_type, error_message, vertices, source = self._resolve(sides)

        self.external_service.send(self.format_result(sides, triangle_type, vertices))

        logging.info(
            "Сценарий завершён: тип=%r, источник=%s, ошибка=%r",
            triangle_type, source, error_message,
        )
        return triangle_type, vertices, error_message, source

    def _resolve(self, sides):
        """Берёт результат из БД, а при промахе считает и сохраняет."""
        cached = self.repository.get(*sides)
        if cached is not None:
            triangle_type, error_message, vertices = cached
            return triangle_type, error_message, vertices, "из БД"

        triangle_type, vertices, error_message = self.calculator.calculate(*sides)
        self.repository.add(sides, triangle_type, vertices, error_message)
        return triangle_type, error_message, vertices, "вычислено"

    @staticmethod
    def format_result(sides, triangle_type, vertices):
        """Собирает строку-результат для отправки стороннему сервису."""
        return "тип={} стороны={} вершины={}".format(
            triangle_type or "(нет данных)", list(sides), vertices
        )