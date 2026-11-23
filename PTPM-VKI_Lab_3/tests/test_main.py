"""Тесты точки входа main.py: сборка зависимостей и обработка сбоев."""

import sqlite3
import unittest
from unittest.mock import patch

import main
from src.calculator import TriangleCalculator
from src.external_service import NotificationService
from src.repository import TriangleRepository
from src.user_interface import ConsoleUserInterface


class TestBuildController(unittest.TestCase):
    """Проверка, что контроллер собирается из настоящих реализаций."""

    def setUp(self):
        # Подменяем путь БД на память, чтобы не создавать файл на диске
        self.patcher = patch.object(main, "DB_PATH", ":memory:")
        self.patcher.start()
        self.controller = main.build_controller()
        self.addCleanup(self.patcher.stop)
        self.addCleanup(self.controller.repository.close)

    def test_controller_receives_real_calculator(self):
        self.assertIsInstance(self.controller.calculator, TriangleCalculator)

    def test_controller_receives_real_repository(self):
        self.assertIsInstance(self.controller.repository, TriangleRepository)

    def test_controller_receives_console_user_interface(self):
        self.assertIsInstance(self.controller.user_interface, ConsoleUserInterface)

    def test_controller_receives_notification_service(self):
        self.assertIsInstance(self.controller.external_service, NotificationService)


class TestMain(unittest.TestCase):
    """Проверка сценариев запуска main() с заглушкой ввода."""

    def test_valid_input_returns_zero_exit_code(self):
        with patch("builtins.input", side_effect=["3", "4", "5"]), \
                patch.object(main, "DB_PATH", ":memory:"):
            self.assertEqual(main.main(), 0)

    def test_invalid_input_returns_nonzero_exit_code(self):
        with patch("builtins.input", side_effect=["abc", "4", "5"]), \
                patch.object(main, "DB_PATH", ":memory:"):
            self.assertEqual(main.main(), 1)

    def test_impossible_sides_return_nonzero_exit_code(self):
        with patch("builtins.input", side_effect=["1", "2", "10"]), \
                patch.object(main, "DB_PATH", ":memory:"):
            self.assertEqual(main.main(), 1)

    def test_unexpected_exception_is_caught_and_logged(self):
        with patch("builtins.input", side_effect=RuntimeError("сбой")), \
                patch.object(main, "DB_PATH", ":memory:"):
            self.assertEqual(main.main(), 1)

    def test_setup_logging_creates_logs_folder_and_attaches_handlers(self):
        import logging

        with patch("os.makedirs") as makedirs_mock:
            main.setup_logging()

        makedirs_mock.assert_called_with("Logs", exist_ok=True)
        handlers = logging.getLogger().handlers
        self.assertTrue(any(isinstance(h, logging.FileHandler) for h in handlers))
        self.assertTrue(any(isinstance(h, logging.StreamHandler) for h in handlers))


if __name__ == "__main__":
    unittest.main(verbosity=2)