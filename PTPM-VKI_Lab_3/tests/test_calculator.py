"""Юнит-тесты класса вычислений TriangleCalculator."""

import unittest

from src.calculator import (
    TYPE_EQUILATERAL,
    TYPE_ISOSCELES,
    TYPE_NOT_TRIANGLE,
    TYPE_SCALENE,
    TriangleCalculator,
)


class TestTriangleCalculator(unittest.TestCase):
    """Проверка метода calculate на всех ветвлениях."""

    def setUp(self):
        self.calculator = TriangleCalculator()

    def test_equal_sides_return_equilateral_type(self):
        self.assertEqual(self.calculator.calculate("5", "5", "5")[0], TYPE_EQUILATERAL)

    def test_two_equal_sides_return_isosceles_type(self):
        self.assertEqual(self.calculator.calculate("5", "5", "8")[0], TYPE_ISOSCELES)

    def test_different_sides_return_scalene_type(self):
        self.assertEqual(self.calculator.calculate("3", "4", "5")[0], TYPE_SCALENE)

    def test_sides_that_violate_inequality_return_not_triangle(self):
        self.assertEqual(self.calculator.calculate("1", "2", "10")[0], TYPE_NOT_TRIANGLE)

    def test_valid_triangle_returns_three_vertices(self):
        self.assertEqual(len(self.calculator.calculate("3", "4", "5")[1]), 3)

    def test_valid_triangle_returns_no_error_message(self):
        self.assertEqual(self.calculator.calculate("3", "4", "5")[2], "")

    def test_vertex_coordinates_are_integers_inside_field(self):
        for x, y in self.calculator.calculate("3", "4", "5")[1]:
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)

    def test_non_numeric_input_returns_minus_two_vertices(self):
        result = self.calculator.calculate("abc", "4", "5")
        self.assertEqual(result[0], "")
        self.assertEqual(result[1], [(-2, -2)] * 3)

    def test_non_numeric_input_returns_error_message(self):
        self.assertNotEqual(self.calculator.calculate("abc", "4", "5")[2], "")

    def test_nan_input_returns_minus_two_vertices(self):
        self.assertEqual(self.calculator.calculate("nan", "4", "5")[1], [(-2, -2)] * 3)

    def test_infinity_input_returns_minus_two_vertices(self):
        self.assertEqual(self.calculator.calculate("inf", "4", "5")[1], [(-2, -2)] * 3)

    def test_zero_side_returns_minus_one_vertices(self):
        self.assertEqual(self.calculator.calculate("3", "0", "5")[1], [(-1, -1)] * 3)

    def test_negative_side_returns_minus_one_vertices(self):
        self.assertEqual(self.calculator.calculate("-3", "4", "5")[1], [(-1, -1)] * 3)

    def test_zero_side_returns_error_message(self):
        self.assertNotEqual(self.calculator.calculate("3", "0", "5")[2], "")

    def test_none_input_returns_minus_two_vertices(self):
        self.assertEqual(self.calculator.calculate(None, "4", "5")[1], [(-2, -2)] * 3)

    def test_very_thin_triangle_does_not_break_sqrt(self):
        result = self.calculator.calculate("10", "10", "19.999999")
        self.assertEqual(len(result[1]), 3)

    def test_degenerate_triangle_with_near_zero_area_is_still_calculated(self):
        triangle_type, vertices, _ = self.calculator.calculate("10", "10", "19.9999999999")
        self.assertEqual(triangle_type, TYPE_ISOSCELES)
        self.assertEqual(len(vertices), 3)
        # Вырожденный треугольник вытянут в линию по оси Y
        self.assertEqual(len({y for _, y in vertices}), 1)

    def test_huge_triangle_is_scaled_into_field(self):
        for x, y in self.calculator.calculate("300", "400", "500")[1]:
            self.assertTrue(0 <= x <= 100)
            self.assertTrue(0 <= y <= 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)