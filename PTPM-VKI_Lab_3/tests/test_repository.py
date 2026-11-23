"""Юнит-тесты класса работы с базой данных TriangleRepository."""

import sqlite3
import unittest

from src.repository import TriangleRepository, decode_vertices, encode_vertices


class TestVertexCodec(unittest.TestCase):
    """Проверка кодирования и восстановления координат."""

    def test_encode_joins_points_into_single_string(self):
        self.assertEqual(encode_vertices([(1, 2), (3, 4)]), "1,2;3,4")

    def test_decode_restores_list_of_tuples(self):
        self.assertEqual(decode_vertices("1,2;3,4"), [(1, 2), (3, 4)])

    def test_encode_and_decode_round_trip(self):
        original = [(5, 89), (95, 89), (50, 11)]
        self.assertEqual(decode_vertices(encode_vertices(original)), original)


class TestTriangleRepository(unittest.TestCase):
    """Проверка операций добавления, чтения и удаления записей."""

    def setUp(self):
        # ":memory:" — база живёт только в памяти, файлы не создаются
        self.connection = sqlite3.connect(":memory:")
        self.repository = TriangleRepository(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_missing_record_returns_none(self):
        self.assertIsNone(self.repository.get("3", "4", "5"))

    def test_count_is_zero_on_empty_table(self):
        self.assertEqual(self.repository.count(), 0)

    def test_added_record_can_be_read_back(self):
        self.repository.add(["3", "4", "5"], "разносторонний", [(1, 2), (3, 4), (5, 6)])
        self.assertEqual(
            self.repository.get("3", "4", "5"),
            ("разносторонний", "", [(1, 2), (3, 4), (5, 6)]),
        )

    def test_error_message_is_stored_together_with_record(self):
        self.repository.add(["abc", "4", "5"], "", [(-2, -2)] * 3, "не число")
        self.assertEqual(self.repository.get("abc", "4", "5")[1], "не число")

    def test_surrounding_whitespace_is_ignored_when_looking_up(self):
        self.repository.add(["3", "4", "5"], "разносторонний", [(1, 1)] * 3)
        self.assertIsNotNone(self.repository.get(" 3 ", "4", "5"))

    def test_repeated_add_replaces_existing_record(self):
        self.repository.add(["3", "4", "5"], "разносторонний", [(1, 1)] * 3)
        self.repository.add(["3", "4", "5"], "разносторонний", [(2, 2)] * 3)
        self.assertEqual(self.repository.count(), 1)
        self.assertEqual(self.repository.get("3", "4", "5")[2], [(2, 2)] * 3)

    def test_different_sides_are_stored_as_separate_records(self):
        self.repository.add(["3", "4", "5"], "разносторонний", [(1, 1)] * 3)
        self.repository.add(["5", "5", "5"], "равносторонний", [(2, 2)] * 3)
        self.assertEqual(self.repository.count(), 2)

    def test_delete_removes_existing_record(self):
        self.repository.add(["3", "4", "5"], "разносторонний", [(1, 1)] * 3)
        self.assertTrue(self.repository.delete("3", "4", "5"))
        self.assertIsNone(self.repository.get("3", "4", "5"))

    def test_delete_returns_false_when_nothing_matched(self):
        self.assertFalse(self.repository.delete("9", "9", "9"))

    def test_none_side_is_treated_as_empty_key(self):
        self.repository.add([None, "4", "5"], "не треугольник", [(-2, -2)] * 3)
        self.assertIsNotNone(self.repository.get(None, "4", "5"))

    def test_close_closes_the_connection(self):
        repository = TriangleRepository(sqlite3.connect(":memory:"))
        repository.close()
        with self.assertRaises(sqlite3.ProgrammingError):
            repository.count()


if __name__ == "__main__":
    unittest.main(verbosity=2)