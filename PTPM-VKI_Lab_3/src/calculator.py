"""Класс вычислений: метод из Лабораторной работы №1."""

import logging
import math

EPS = 1e-9
FLAT_EPS = 1e-6  # площадь ближе этого значения считаем вырожденной
FIELD_SIZE = 100
PADDING = 5

INVALID_NUMERIC = [(-1, -1), (-1, -1), (-1, -1)]
INVALID_INPUT = [(-2, -2), (-2, -2), (-2, -2)]

TYPE_EQUILATERAL = "равносторонний"
TYPE_ISOSCELES = "равнобедренный"
TYPE_SCALENE = "разносторонний"
TYPE_NOT_TRIANGLE = "не треугольник"


def _is_valid_number(value):
    """Проверяет, что значение — конечное положительно пригодное число.

    float() принимает nan и inf, но считать по ним нельзя, поэтому
    используется math.isfinite().
    """
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def _classify(a, b, c):
    """Определяет вид треугольника по трём сторонам."""
    if a + b <= c or a + c <= b or b + c <= a:
        logging.warning("Треугольник %s, %s, %s не существует", a, b, c)
        return TYPE_NOT_TRIANGLE

    eq_ab = math.isclose(a, b, abs_tol=EPS)
    eq_ac = math.isclose(a, c, abs_tol=EPS)
    eq_bc = math.isclose(b, c, abs_tol=EPS)

    if eq_ab and eq_ac:
        return TYPE_EQUILATERAL
    if eq_ab or eq_ac or eq_bc:
        return TYPE_ISOSCELES
    return TYPE_SCALENE


def _vertices(a, b, c):
    """Считает координаты трёх вершин в поле 100x100 px."""
    # Длинная сторона кладётся на ось X, третья вершина — по теореме косинусов
    ax, ay = 0.0, 0.0
    bx, by = a, 0.0
    cx = (a * a + b * b - c * c) / (2.0 * a)
    cy_sq = b * b - cx * cx

    if cy_sq < FLAT_EPS:
        logging.warning("Вырожденный треугольник %s, %s, %s: площадь близка к нулю", a, b, c)
    # max защищает: sqrt от отрицательного числа падает
    cy = math.sqrt(max(cy_sq, 0.0))

    # Ограничивающий прямоугольник фигуры
    min_x, max_x = min(ax, bx, cx), max(ax, bx, cx)
    min_y, max_y = min(ay, by, cy), max(ay, by, cy)
    width, height = max_x - min_x, max_y - min_y

    field = FIELD_SIZE - 2 * PADDING  # доступная зона 90x90
    scale = 1.0
    if width > 0:
        scale = min(scale, field / width)
    if height > 0:
        scale = min(scale, field / height)

    # Центрируем по полю
    cx_center = (min_x + max_x) / 2.0
    cy_center = (min_y + max_y) / 2.0
    center = PADDING + field / 2.0

    def to_px(x, y):
        px = int(round(center + (x - cx_center) * scale))
        py = int(round(center + (y - cy_center) * scale))
        return (max(0, min(FIELD_SIZE, px)), max(0, min(FIELD_SIZE, py)))

    result = [to_px(ax, ay), to_px(bx, by), to_px(cx, cy)]
    logging.info("Координаты рассчитаны: %s", result)
    return result


class TriangleCalculator:
    """Вычисляет вид треугольника и координаты его вершин."""

    def calculate(self, line_a, line_b, line_c):
        """Возвращает (тип треугольника, список координат вершин, текст ошибки)."""
        lines = (line_a, line_b, line_c)

        # Нечисловые данные и nan/inf -> пустой тип, координаты (-2,-2)
        if not all(_is_valid_number(line) for line in lines):
            logging.warning("Нечисловые входные данные: %s", lines)
            return "", list(INVALID_INPUT), "входные данные не являются числами"

        a, b, c = float(line_a), float(line_b), float(line_c)
        logging.debug("Стороны разобраны: a=%s, b=%s, c=%s", a, b, c)

        # Неположительные числа -> координаты (-1,-1)
        if a <= 0 or b <= 0 or c <= 0:
            logging.warning("Неположительные стороны: a=%s, b=%s, c=%s", a, b, c)
            return TYPE_NOT_TRIANGLE, list(INVALID_NUMERIC), "длины сторон должны быть положительными"

        triangle_type = _classify(a, b, c)

        if triangle_type == TYPE_NOT_TRIANGLE:
            logging.warning("Нарушено неравенство треугольника")
            return TYPE_NOT_TRIANGLE, list(INVALID_NUMERIC), "стороны не образуют треугольник"

        return triangle_type, _vertices(a, b, c), ""