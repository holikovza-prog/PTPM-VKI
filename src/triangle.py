import logging
import math

# Маленькое число для сравнения float-ов (погрешность)
EPS = 1e-9


def _is_float(value: str) -> bool:
    """Проверяет, что строка — корректное вещественное число."""
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def _classify_triangle(a: float, b: float, c: float) -> str:
    """Определяет вид треугольника по трём сторонам."""
    # Неравенство треугольника
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"

    # Сравнения с учётом погрешности float
    eq_ab = math.isclose(a, b, abs_tol=EPS)
    eq_ac = math.isclose(a, c, abs_tol=EPS)
    eq_bc = math.isclose(b, c, abs_tol=EPS)

    if eq_ab and eq_ac:
        return "равносторонний"
    if eq_ab or eq_ac or eq_bc:
        return "равнобедренный"
    return "разносторонний"


def _calc_vertices(a: float, b: float, c: float) -> list:
    """
    Вычисляет координаты 3 вершин треугольника
    и вписывает их в поле 100x100 px.
    """
    # A в начале координат, B на оси X
    ax, ay = 0.0, 0.0
    bx, by = a, 0.0

    # Координаты C по теореме косинусов
    cx = (a * a + b * b - c * c) / (2.0 * a)
    cy_sq = b * b - cx * cx
    cy = math.sqrt(cy_sq) if cy_sq > 0 else 0.0

    # Текущие границы (bounding box) треугольника
    xs = [ax, bx, cx]
    ys = [ay, by, cy]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    width = max_x - min_x
    height = max_y - min_y

    # Поле 100x100 с отступом по 5 px с каждой стороны
    padding = 5
    field = 100 - 2 * padding  # доступная зона 90x90

    # Масштаб — чтобы треугольник влез по обеим осям
    scale = 1.0
    if width > 0:
        scale = min(scale, field / width)
    if height > 0:
        scale = min(scale, field / height)

    # Центрирование: сдвигаем так, чтобы центр bbox попал в центр поля
    cx_center = (min_x + max_x) / 2.0
    cy_center = (min_y + max_y) / 2.0
    field_center = padding + field / 2.0  # = 50

    def to_px(x, y):
        return (
            int(round(field_center + (x - cx_center) * scale)),
            int(round(field_center + (y - cy_center) * scale)),
        )

    return [to_px(ax, ay), to_px(bx, by), to_px(cx, cy)]


def process_triangle(line_a: str, line_b: str, line_c: str):
    """
    Главная функция обработки.
    Возвращает кортеж (тип_треугольника, список_координат).
    """
    # --- Проверка на нечисловые данные ---
    if not (_is_float(line_a) and _is_float(line_b) and _is_float(line_c)):
        logging.warning("Получены нечисловые входные данные")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    a, b, c = float(line_a), float(line_b), float(line_c)

    # --- Проверка на положительность ---
    if a <= 0 or b <= 0 or c <= 0:
        logging.warning(f"Некорректные значения сторон: a={a}, b={b}, c={c}")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    # --- Классификация ---
    triangle_type = _classify_triangle(a, b, c)

    # --- Координаты ---
    if triangle_type == "не треугольник":
        # Ошибочные числовые данные → сброс координат в (-1, -1)
        vertices = [(-1, -1), (-1, -1), (-1, -1)]
    else:
        vertices = _calc_vertices(a, b, c)

    return triangle_type, vertices