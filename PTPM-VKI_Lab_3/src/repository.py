"""Класс работы с базой данных SQLite."""

import logging
import sqlite3


def encode_vertices(vertices):
    """Кодирует список кортежей в строку для хранения в БД: 'x1,y1;x2,y2;x3,y3'."""
    return ";".join(f"{x},{y}" for x, y in vertices)


def decode_vertices(raw):
    """Восстанавливает список кортежей из строки, полученной из БД."""
    vertices = []
    for pair in raw.split(";"):
        x, y = pair.split(",")
        vertices.append((int(x), int(y)))
    return vertices


class TriangleRepository:
    """Хранит рассчитанные треугольники в таблице SQLite."""

    def __init__(self, connection):
        self._connection = connection
        self._create_table()

    def _create_table(self):
        """Создаёт таблицу, если её ещё нет. Запись опознаётся по трём длинам."""
        with self._connection:
            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS triangles (
                    side1         TEXT NOT NULL,
                    side2         TEXT NOT NULL,
                    side3         TEXT NOT NULL,
                    triangle_type TEXT NOT NULL,
                    error_message TEXT NOT NULL DEFAULT '',
                    vertices      TEXT NOT NULL,
                    PRIMARY KEY (side1, side2, side3)
                )
                """
            )
        logging.info("Таблица triangles готова")

    @staticmethod
    def _key(sides):
        """Приводит стороны к ключу: обрезает пробелы, None заменяет пустой строкой."""
        return tuple((side or "").strip() for side in sides)

    def add(self, sides, triangle_type, vertices, error_message=""):
        """Добавляет или перезаписывает запись для трёх сторон."""
        key = self._key(sides)
        with self._connection:
            self._connection.execute(
                "INSERT OR REPLACE INTO triangles "
                "(side1, side2, side3, triangle_type, error_message, vertices) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                key + (triangle_type, error_message, encode_vertices(vertices)),
            )
        logging.info("Записана запись: %s -> %s", key, triangle_type)

    def get(self, side1, side2, side3):
        """Возвращает (тип, текст ошибки, координаты) или None, если записи нет."""
        key = self._key((side1, side2, side3))
        cursor = self._connection.execute(
            "SELECT triangle_type, error_message, vertices FROM triangles "
            "WHERE side1 = ? AND side2 = ? AND side3 = ?",
            key,
        )
        row = cursor.fetchone()
        if row is None:
            logging.info("Запись %s не найдена в БД", key)
            return None

        logging.info("Найдена запись %s в БД", key)
        return row[0], row[1], decode_vertices(row[2])

    def delete(self, side1, side2, side3):
        """Удаляет запись. Возвращает True, если что-то было удалено."""
        key = self._key((side1, side2, side3))
        with self._connection:
            cursor = self._connection.execute(
                "DELETE FROM triangles WHERE side1 = ? AND side2 = ? AND side3 = ?",
                key,
            )
        deleted = cursor.rowcount > 0
        logging.info("Удаление %s: выполнено=%s", key, deleted)
        return deleted

    def count(self):
        """Возвращает общее количество записей в таблице."""
        cursor = self._connection.execute("SELECT COUNT(*) FROM triangles")
        return cursor.fetchone()[0]

    def close(self):
        """Закрывает соединение с базой."""
        self._connection.close()
        logging.info("Соединение с БД закрыто")