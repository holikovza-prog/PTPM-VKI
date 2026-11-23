"""Точка входа лабораторной работы №3: интеграционное тестирование и заглушки."""

import logging
import os
import sqlite3
import sys

from src.controller import Controller
from src.calculator import TriangleCalculator
from src.external_service import NotificationService
from src.repository import TriangleRepository
from src.user_interface import ConsoleUserInterface

LOG_FORMAT = "%(asctime)s | [%(levelname)-7s] | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DB_PATH = "triangles.db"


def setup_logging():
    """Настраивает параллельный вывод логов в консоль и файл."""
    os.makedirs("Logs", exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(os.path.join("Logs", "file_txt.log"), encoding="utf-8"),
        ],
        force=True,
    )
    logging.info("Логгер успешно сконфигурирован")


def build_controller(db_path=DB_PATH):
    """Собирает контроллер из настоящих реализаций всех зависимостей."""
    connection = sqlite3.connect(db_path)
    return Controller(
        calculator=TriangleCalculator(),
        repository=TriangleRepository(connection),
        user_interface=ConsoleUserInterface(),
        external_service=NotificationService(),
    )


def main():
    setup_logging()
    logging.info("Приложение запущено")

    try:
        controller = build_controller()
        triangle_type, vertices, error_message, source = controller.run()
    except Exception as error:
        logging.error("Сценарий не выполнен: %s: %s", type(error).__name__, error)
        logging.exception("Трассировка:")
        return 1

    print(f"Тип треугольника: {triangle_type or '(нет данных)'}")
    print(f"Координаты вершин: {vertices}")
    print(f"Сообщение об ошибке: {error_message or '-'}")
    print(f"Источник результата: {source}")

    controller.repository.close()
    logging.info("Приложение завершено")
    return 0 if triangle_type and error_message == "" else 1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover