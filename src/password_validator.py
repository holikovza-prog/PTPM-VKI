"""Модуль валидации пароля согласно политикам безопасности."""

SPECIAL_CHARACTERS = frozenset("!@#$%^&*")


def validate_password(password: str) -> bool:
    """
    Выполняет валидацию строки пароля на соответствие политикам безопасности.

    :param password: Проверяемый пароль
    :return: True, если пароль удовлетворяет всем условиям, иначе False
    :raises TypeError: Если входной параметр не является строкой
    :raises ValueError: Если входная строка содержит символы пробела
    """
    if not isinstance(password, str):
        raise TypeError("Пароль должен быть строкой")

    if " " in password:
        raise ValueError("Пароль не должен содержать пробелы")

    if not (8 <= len(password) <= 20):
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for ch in password:
        if ch.isupper():
            has_upper = True
        if ch.islower():
            has_lower = True
        if ch.isdigit():
            has_digit = True
        if ch in SPECIAL_CHARACTERS:
            has_special = True

    return has_upper and has_lower and has_digit and has_special