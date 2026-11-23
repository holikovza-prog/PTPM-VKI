"""Юнит-тесты интерфейсов пользователя и внешнего сервиса."""

import unittest
from unittest.mock import patch

from src.external_service import ExternalService, NotificationService
from src.user_interface import ConsoleUserInterface, UserInterface


class TestUserInterfaceContract(unittest.TestCase):
    """Проверка того, что абстрактный класс действительно запрещает создание."""

    def test_abstract_interface_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            UserInterface()

    def test_console_implementation_is_instance_of_interface(self):
        self.assertIsInstance(ConsoleUserInterface(), UserInterface)


class TestConsoleUserInterface(unittest.TestCase):
    """Проверка чтения данных через input() с заглушкой."""

    def test_three_entered_lines_are_returned(self):
        with patch("builtins.input", side_effect=["3", "4", "5"]):
            self.assertEqual(ConsoleUserInterface().get_sides(), ["3", "4", "5"])

    def test_interrupted_input_produces_empty_string(self):
        with patch("builtins.input", side_effect=["3", EOFError(), "5"]):
            self.assertEqual(ConsoleUserInterface().get_sides(), ["3", "", "5"])


class TestExternalServiceContract(unittest.TestCase):
    """Проверка абстрактного интерфейса внешней зависимости."""

    def test_abstract_service_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            ExternalService()

    def test_notification_service_is_instance_of_interface(self):
        self.assertIsInstance(NotificationService(), ExternalService)


class TestNotificationService(unittest.TestCase):
    """Проверка имитации отправки данных."""

    def test_send_returns_true_on_success(self):
        self.assertTrue(NotificationService().send("результат"))

    def test_sent_message_is_kept_in_list(self):
        service = NotificationService()
        service.send("первое")
        service.send("второе")
        self.assertEqual(service.sent, ["первое", "второе"])

    def test_fresh_service_has_empty_sent_list(self):
        self.assertEqual(NotificationService().sent, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)