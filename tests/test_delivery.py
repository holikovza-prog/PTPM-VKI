"""
Юнит-тесты для модуля src.Delivery (расчёт стоимости доставки).
Запуск: python -m unittest discover -v
"""
import unittest
from src.Delivery import calculate_delivery_cost


class TestDeliveryHappyPath(unittest.TestCase):
    """Корректные сценарии (должны проходить успешно)."""

    def test_base_cost_and_distance_calculation(self):
        # 200 (база) + 100 * 5 (дистанция) = 700
        # 100 // 500 = 0 -> max(1, 0) = 1 день. 03.09 + 1 день = 04.09
        cost, date = calculate_delivery_cost(2.0, 100, "обычный", False)
        self.assertEqual(cost, 700)
        self.assertEqual(date, "2026-09-04")

    def test_medium_weight_multiplier(self):
        # 700 * 1.2 = 840
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный", False)
        self.assertEqual(cost, 840)

    def test_heavy_weight_multiplier(self):
        # 700 * 1.5 = 1050
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный", False)
        self.assertEqual(cost, 1050)

    def test_fragile_package_surcharge(self):
        # 700 + 300 = 1000
        cost, _ = calculate_delivery_cost(2.0, 100, "хрупкий", False)
        self.assertEqual(cost, 1000)

    def test_dangerous_package_surcharge(self):
        # 700 + 1000 = 1700
        cost, _ = calculate_delivery_cost(2.0, 100, "опасный", False)
        self.assertEqual(cost, 1700)

    def test_long_distance_increases_days(self):
        # 1000 // 500 = 2 дня. 03.09 + 2 дня = 05.09
        _, date = calculate_delivery_cost(2.0, 1000, "обычный", False)
        self.assertEqual(date, "2026-09-05")


class TestDeliveryValidation(unittest.TestCase):
    """Валидация входных данных (должна проходить успешно)."""

    def test_invalid_weight_below_minimum(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный", False)
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_invalid_weight_above_maximum(self):
        cost, date = calculate_delivery_cost(50.1, 100, "обычный", False)
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_invalid_distance_zero(self):
        cost, date = calculate_delivery_cost(2.0, 0, "обычный", False)
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_invalid_distance_too_far(self):
        cost, date = calculate_delivery_cost(2.0, 5001, "обычный", False)
        self.assertEqual((cost, date), (-1, "0000-00-00"))

    def test_invalid_package_type(self):
        cost, date = calculate_delivery_cost(5.0, 100, "секретный", False)
        self.assertEqual((cost, date), (-1, "0000-00-00"))


class TestDeliveryKnownBugs(unittest.TestCase):
    """
    ⚠️ НАМЕРЕННО ПАДАЮЩИЕ ТЕСТЫ.
    Фиксируются в Пункте В отчета как найденные дефекты.
    """

    def test_express_delivery_should_increase_cost(self):
        """БАГ 1: Экспресс должен УВЕЛИЧИВАТЬ стоимость (*1.5), а не уменьшать (*0.5)."""
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный", True)
        # 700 * 1.2 = 840. Ожидаем 840 * 1.5 = 1260. Код вернет 420.
        self.assertEqual(cost, 1260)

    def test_express_delivery_minimum_one_day(self):
        """БАГ 2: Экспресс не может занимать 0 дней — минимум 1."""
        _, date = calculate_delivery_cost(2.0, 400, "обычный", True)
        # 400 // 500 = 0 -> max(1, 0) = 1. Экспресс: 1 // 2 = 0 (баг).
        # Ожидаем 1 день. Код вернет 03.09 (0 дней).
        self.assertEqual(date, "2026-09-04")

    def test_weight_boundary_exactly_5kg_should_apply_multiplier(self):
        """БАГ 3: Вес ровно 5.0 кг должен попадать под коэффициент 1.2."""
        cost_5_0, _ = calculate_delivery_cost(5.0, 100, "обычный", False)
        # Ожидаем 700 * 1.2 = 840. Код вернет 700 (т.к. условие > 5.0, а не >=).
        self.assertEqual(cost_5_0, 840)


if __name__ == "__main__":
    unittest.main()