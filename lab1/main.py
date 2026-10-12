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
    level=logging.INFO,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("Logs/file_txt.log", encoding="utf-8"),
    ],
)


def main():
    logging.info("Приложение запущено")
    print("Вводите стороны треугольника. Для выхода введите 'q' в поле A.")

    while True:
        try:
            line_a = input("Введите сторону A (или 'q' для выхода): ").strip()
            if line_a.lower() == "q":
                break

            line_b = input("Введите сторону B: ").strip()
            line_c = input("Введите сторону C: ").strip()

        except (EOFError, KeyboardInterrupt):
            print()  # перевод строки после ^C / ^D
            logging.warning("Ввод прерван пользователем")
            break

        logging.info(f"Запрос: a={line_a!r}, b={line_b!r}, c={line_c!r}")

        try:
            triangle_type, vertices = process_triangle(line_a, line_b, line_c)
            logging.info(
                f"Результат: тип='{triangle_type}', координаты={vertices}"
            )
            print(f"  → Тип: {triangle_type}")
            print(f"  → Координаты: {vertices}")
        except (ValueError, TypeError) as ex:
            logging.error(f"Ошибка обработки запроса: {ex}")
            logging.exception("Трассировка:")

        print()  # пустая строка для читаемости

    logging.info("Приложение завершено")


if __name__ == "__main__":
    main()