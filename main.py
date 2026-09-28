import logging
import sys
import os

from triangle import process_triangle

# --- 1. Создаём папку для логов, если её нет ---
os.makedirs("Logs", exist_ok=True)

# --- 2. Настраиваем логгер (в консоль + в файл одновременно) ---
log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,                       # минимальный уровень — DEBUG
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),                         # в консоль
        logging.FileHandler("Logs/file_txt.log", encoding="utf-8") # в файл
    ]
)


def main():
    logging.info("Приложение запущено")

    # Имитация входных данных — три строки от пользователя
    # Можно заменить на input() при желании
    raw_inputs = [
        ("3", "4", "5"),          # разносторонний
        ("5", "5", "5"),          # равносторонний
        ("5", "5", "8"),          # равнобедренный
        ("1", "2", "10"),         # не треугольник
        ("abc", "4", "5"),        # нечисловые данные
        ("-1", "4", "5"),         # отрицательная сторона
    ]

    for line_a, line_b, line_c in raw_inputs:
        logging.info(f"Запрос: a={line_a!r}, b={line_b!r}, c={line_c!r}")

        try:
            triangle_type, vertices = process_triangle(line_a, line_b, line_c)

            logging.info(
                f"Результат: тип='{triangle_type}', "
                f"координаты={vertices}"
            )

        except Exception as ex:
            # На всякий случай — сюда мы попадать не должны,
            # вся валидация внутри process_triangle
            logging.error("Непредвиденная ошибка при обработке запроса")
            logging.exception("Трассировка:")

    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()