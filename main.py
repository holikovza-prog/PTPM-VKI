import logging
import sys
import os

from triangle import process_triangle

# Создаём папку для логов, если её нет
os.makedirs("Logs", exist_ok=True)

# Настраиваем логгер: в консоль + в файл одновременно
log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("Logs/file_txt.log", encoding="utf-8"),
    ],
)


def main():
    logging.info("Приложение запущено")

    raw_inputs = [
        ("3", "4", "5"),
        ("5", "5", "5"),
        ("5", "5", "8"),
        ("1", "2", "10"),
        ("abc", "4", "5"),
        ("-1", "4", "5"),
    ]

    for line_a, line_b, line_c in raw_inputs:
        logging.info(f"Запрос: a={line_a!r}, b={line_b!r}, c={line_c!r}")

        try:
            triangle_type, vertices = process_triangle(line_a, line_b, line_c)
            logging.info(
                f"Результат: тип='{triangle_type}', координаты={vertices}"
            )

        except (ValueError, TypeError) as ex:
            logging.error(f"Ошибка обработки запроса: {ex}")
            logging.exception("Трассировка:")

    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()