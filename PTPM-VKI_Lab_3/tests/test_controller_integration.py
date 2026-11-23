"""Интеграционные тесты: реальные вычисления и БД, заглушки ввода и внешнего сервиса.

Изоляция модулей проверяется через unittest.mock:
  * пользовательский ввод подменяется Mock на стороне UserInterface;
  * отправка во внешний сервис подменяется Mock на стороне ExternalService.
Вычисления и база данных при этом остаются настоящими.
"""

import sqlite3
import unittest
from unittest.mock import Mock, patch

from src.calculator import TriangleCalculator
from src.controller import Controller
from src.repository import TriangleRepository
from src.external_service import ExternalService
from src.user_interface import UserInterface


class ControllerIntegrationTestCase(unittest.TestCase):
    """Общая настройка: настоящие калькулятор и БД, заглушки вместо I/O."""

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.repository = TriangleRepository(self.connection)
        self.calculator = TriangleCalculator()

        # Заглушка пользовательского ввода
        self.ui_mock = Mock(spec=UserInterface)
        # Заглушка внешнего сервиса
        self.external_mock = Mock(spec=ExternalService)
        self.external_mock.send.return_value = True

        self.controller = Controller(
            calculator=self.calculator,
            repository=self.repository,
            user_interface=self.ui_mock,
            external_service=self.external_mock,
        )

    def tearDown(self):
        self.connection.close()


class TestControllerFullScenario(ControllerIntegrationTestCase):
    """Сквозной сценарий целиком."""

    def test_new_triangle_is_computed_and_saved_to_database(self):
        self.ui_mock.get_sides.return_value = ["3", "4", "5"]

        triangle_type, vertices, error_message, source = self.controller.run()

        self.assertEqual(triangle_type, "разносторонний")
        self.assertEqual(len(vertices), 3)
        self.assertEqual(error_message, "")
        self.assertEqual(source, "вычислено")
        self.assertEqual(self.repository.count(), 1)

    def test_second_request_for_same_sides_takes_result_from_database(self):
        self.ui_mock.get_sides.return_value = ["3", "4", "5"]

        self.controller.run()
        second_type, second_vertices, _, second_source = self.controller.run()

        self.assertEqual(second_source, "из БД")
        self.assertEqual(second_type, "разносторонний")
        self.assertEqual(second_vertices, self.repository.get("3", "4", "5")[2])

    def test_cached_result_does_not_trigger_recalculation(self):
        self.ui_mock.get_sides.return_value = ["5", "5", "5"]
        self.controller.run()

        with patch.object(self.calculator, "calculate") as calculate_spy:
            self.controller.run()

        calculate_spy.assert_not_called()

    def test_result_string_is_sent_to_external_service(self):
        self.ui_mock.get_sides.return_value = ["3", "4", "5"]

        self.controller.run()

        self.external_mock.send.assert_called_once()
        message = self.external_mock.send.call_args[0][0]
        self.assertIn("разносторонний", message)
        self.assertIn("['3', '4', '5']", message)

    def test_invalid_input_does_not_break_the_scenario(self):
        self.ui_mock.get_sides.return_value = ["abc", "4", "5"]

        triangle_type, vertices, error_message, source = self.controller.run()

        self.assertEqual(triangle_type, "")
        self.assertEqual(vertices, [(-2, -2)] * 3)
        self.assertNotEqual(error_message, "")
        self.assertEqual(source, "вычислено")
        self.external_mock.send.assert_called_once()

    def test_impossible_sides_are_cached_with_error_message(self):
        self.ui_mock.get_sides.return_value = ["1", "2", "10"]

        triangle_type, vertices, error_message, _ = self.controller.run()

        self.assertEqual(triangle_type, "не треугольник")
        self.assertEqual(vertices, [(-1, -1)] * 3)
        self.assertEqual(self.repository.get("1", "2", "10")[1], error_message)

    def test_deleting_cached_record_forces_recalculation(self):
        self.ui_mock.get_sides.return_value = ["3", "4", "5"]
        self.controller.run()

        self.repository.delete("3", "4", "5")
        _, _, _, source = self.controller.run()

        self.assertEqual(source, "вычислено")

    def test_different_requests_are_cached_separately(self):
        self.ui_mock.get_sides.return_value = ["3", "4", "5"]
        self.controller.run()
        self.ui_mock.get_sides.return_value = ["5", "5", "5"]
        self.controller.run()

        self.assertEqual(self.repository.count(), 2)
        self.assertEqual(self.repository.get("5", "5", "5")[0], "равносторонний")

    def test_failed_external_send_does_not_affect_returned_result(self):
        self.external_mock.send.return_value = False
        self.ui_mock.get_sides.return_value = ["3", "4", "5"]

        triangle_type, _, _, source = self.controller.run()

        self.assertEqual(triangle_type, "разносторонний")
        self.assertEqual(source, "вычислено")

    def test_user_interface_is_queried_exactly_once_per_run(self):
        self.ui_mock.get_sides.return_value = ["3", "4", "5"]

        self.controller.run()

        self.ui_mock.get_sides.assert_called_once_with()


if __name__ == "__main__":
    unittest.main(verbosity=2)