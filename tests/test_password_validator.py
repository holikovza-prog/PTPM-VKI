import unittest

from src.password_validator import validate_password


class TestPasswordValidator(unittest.TestCase):
    # ---------------------------------------------------------------
    # 1. Позитивное тестирование
    # ---------------------------------------------------------------

    def test_valid_password_latin(self):
        self.assertTrue(validate_password("SecurePass1!"))

    def test_valid_password_cyrillic(self):
        self.assertTrue(validate_password("ПарольТест9#"))

    # ---------------------------------------------------------------
    # 2. Анализ граничных значений длины
    # ---------------------------------------------------------------

    def test_length_7_below_minimum(self):
        # Длина 7: на 1 меньше нижней границы
        self.assertFalse(validate_password("Aa1!aaa"))

    def test_length_8_minimum_boundary(self):
        # Длина 8: нижняя граница
        self.assertTrue(validate_password("Aa1!aaaa"))

    def test_length_20_maximum_boundary(self):
        # Длина 20: верхняя граница
        password = "Aa1!" + "a" * 16
        self.assertTrue(validate_password(password))

    def test_length_21_above_maximum(self):
        # Длина 21: на 1 больше верхней границы
        password = "Aa1!" + "a" * 17
        self.assertFalse(validate_password(password))

    # ---------------------------------------------------------------
    # 3. Классы эквивалентности: неполный состав символов
    # ---------------------------------------------------------------

    def test_missing_uppercase(self):
        self.assertFalse(validate_password("securepass1!"))

    def test_missing_lowercase(self):
        self.assertFalse(validate_password("SECUREPASS1!"))

    def test_missing_digit(self):
        self.assertFalse(validate_password("SecurePassword!"))

    def test_missing_special(self):
        self.assertFalse(validate_password("SecurePassword1"))

    def test_invalid_special_char_underscore(self):
        self.assertFalse(validate_password("SecurePass1_"))

    def test_invalid_special_char_question(self):
        self.assertFalse(validate_password("SecurePass1?"))

    def test_empty_string(self):
        self.assertFalse(validate_password(""))

    # ---------------------------------------------------------------
    # 4. Исключения: пробелы
    # ---------------------------------------------------------------

    def test_value_error_space_inside(self):
        with self.assertRaises(ValueError) as context:
            validate_password("Pass 1234!")
        self.assertEqual(
            str(context.exception),
            "Пароль не должен содержать пробелы",
        )

    def test_value_error_space_at_start(self):
        with self.assertRaises(ValueError) as context:
            validate_password(" Pass1234!")
        self.assertEqual(
            str(context.exception),
            "Пароль не должен содержать пробелы",
        )

    def test_value_error_space_at_end(self):
        with self.assertRaises(ValueError) as context:
            validate_password("Pass1234! ")
        self.assertEqual(
            str(context.exception),
            "Пароль не должен содержать пробелы",
        )

    # ---------------------------------------------------------------
    # 5. Исключения: некорректный тип аргумента
    # ---------------------------------------------------------------

    def test_type_error_none(self):
        with self.assertRaises(TypeError) as context:
            validate_password(None)
        self.assertEqual(
            str(context.exception),
            "Пароль должен быть строкой",
        )

    def test_type_error_int(self):
        with self.assertRaises(TypeError) as context:
            validate_password(12345678)
        self.assertEqual(
            str(context.exception),
            "Пароль должен быть строкой",
        )

    def test_type_error_list(self):
        with self.assertRaises(TypeError) as context:
            validate_password(["P", "a", "s", "s", "1", "!"])
        self.assertEqual(
            str(context.exception),
            "Пароль должен быть строкой",
        )


if __name__ == "__main__":
    unittest.main()