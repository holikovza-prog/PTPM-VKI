"""
Юнит-тесты для модуля src.my_project (ЛР1: классификация треугольников).
Запуск: python -m unittest tests.test_my_project -v
"""
import unittest

from src.my_project import (
    process_triangle,
    _classify_triangle,
    _calc_vertices,
    _is_float,
)


class TestIsFloatHelper(unittest.TestCase):
    """Тесты вспомогательной функции _is_float."""

    def test_is_float_accepts_integer_string(self):
        self.assertTrue(_is_float("42"))

    def test_is_float_accepts_negative_decimal(self):
        self.assertTrue(_is_float("-3.14"))

    def test_is_float_accepts_scientific_notation(self):
        self.assertTrue(_is_float("1e-3"))

    def test_is_float_rejects_letters(self):
        self.assertFalse(_is_float("abc"))

    def test_is_float_rejects_empty_string(self):
        self.assertFalse(_is_float(""))


class TestInputValidation(unittest.TestCase):
    """Тесты валидации входных данных в process_triangle."""

    def test_non_numeric_first_arg_returns_error_code(self):
        result = process_triangle("abc", "4", "5")
        self.assertEqual(result, ("", [(-2, -2), (-2, -2), (-2, -2)]))

    def test_non_numeric_second_arg_returns_error_code(self):
        result = process_triangle("3", "xyz", "5")
        self.assertEqual(result[0], "")
        self.assertEqual(result[1], [(-2, -2), (-2, -2), (-2, -2)])

    def test_non_numeric_third_arg_returns_error_code(self):
        result = process_triangle("3", "4", "??")
        self.assertEqual(result[0], "")

    def test_empty_string_returns_error_code(self):
        result = process_triangle("", "", "")
        self.assertEqual(result[0], "")

    def test_zero_side_returns_not_triangle(self):
        result = process_triangle("0", "4", "5")
        self.assertEqual(result[0], "не треугольник")
        self.assertEqual(result[1], [(-1, -1), (-1, -1), (-1, -1)])

    def test_negative_side_returns_not_triangle(self):
        result = process_triangle("-3", "4", "5")
        self.assertEqual(result[0], "не треугольник")
        self.assertEqual(result[1], [(-1, -1), (-1, -1), (-1, -1)])


class TestTriangleClassification(unittest.TestCase):
    """Тесты классификации треугольников через process_triangle."""

    def test_equilateral_returns_correct_type(self):
        self.assertEqual(process_triangle("5", "5", "5")[0], "равносторонний")

    def test_equilateral_float_values(self):
        self.assertEqual(process_triangle("5.0", "5.0", "5.0")[0], "равносторонний")

    def test_isosceles_ab_equal(self):
        self.assertEqual(process_triangle("5", "5", "8")[0], "равнобедренный")

    def test_isosceles_bc_equal(self):
        self.assertEqual(process_triangle("6", "8", "8")[0], "равнобедренный")

    def test_isosceles_ac_equal(self):
        self.assertEqual(process_triangle("7", "9", "7")[0], "равнобедренный")

    def test_scalene_triangle(self):
        self.assertEqual(process_triangle("3", "4", "5")[0], "разносторонний")

    def test_degenerate_returns_not_triangle(self):
        # 2 + 3 == 5 → вырожденный
        self.assertEqual(process_triangle("2", "3", "5")[0], "не треугольник")

    def test_inequality_violation_returns_not_triangle(self):
        # 1 + 2 < 10
        self.assertEqual(process_triangle("1", "2", "10")[0], "не треугольник")

    def test_not_triangle_returns_minus_one_vertices(self):
        _, vertices = process_triangle("1", "2", "10")
        self.assertEqual(vertices, [(-1, -1), (-1, -1), (-1, -1)])


class TestVerticesComputation(unittest.TestCase):
    """Тесты расчёта координат вершин _calc_vertices."""

    def test_vertices_count_is_three(self):
        vertices = _calc_vertices(3.0, 4.0, 5.0)
        self.assertEqual(len(vertices), 3)

    def test_all_vertices_inside_field(self):
        vertices = _calc_vertices(3.0, 4.0, 5.0)
        for x, y in vertices:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_large_triangle_is_scaled_inside_field(self):
        vertices = _calc_vertices(1000.0, 1000.0, 1000.0)
        for x, y in vertices:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_small_triangle_not_upscaled_beyond_field(self):
        vertices = _calc_vertices(0.001, 0.001, 0.001)
        self.assertEqual(len(vertices), 3)
        for x, y in vertices:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)

    def test_equilateral_vertices_are_symmetric(self):
        # У равностороннего треугольника вершина C лежит на оси симметрии (x ≈ 50)
        vertices = _calc_vertices(5.0, 5.0, 5.0)
        cx = vertices[2][0]
        self.assertAlmostEqual(cx, 50, delta=2)

    def test_vertices_are_integer_tuples(self):
        vertices = _calc_vertices(3.0, 4.0, 5.0)
        for point in vertices:
            self.assertIsInstance(point, tuple)
            self.assertIsInstance(point[0], int)
            self.assertIsInstance(point[1], int)


class TestClassifyTriangleDirect(unittest.TestCase):
    """Прямые тесты _classify_triangle (без process_triangle)."""

    def test_right_triangle_is_scalene(self):
        # 3-4-5 — прямоугольный, но по сторонам разносторонний
        self.assertEqual(_classify_triangle(3.0, 4.0, 5.0), "разносторонний")

    def test_almost_equal_sides_isosceles(self):
        # Погрешность float: 5.0 и 5.0+1e-12 считаются равными
        self.assertEqual(_classify_triangle(5.0, 5.0 + 1e-12, 8.0), "равнобедренный")

    def test_all_zero_sides_not_triangle(self):
        self.assertEqual(_classify_triangle(0.0, 0.0, 0.0), "не треугольник")


if __name__ == "__main__":
    unittest.main()