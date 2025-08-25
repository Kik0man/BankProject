import pytest

from typing import Any


# Ниже идут фикстуры для проверки 3 модулей: masks.py \ processing.py \ widget.py
@pytest.fixture
def card_info() -> list[str]:
    """Функция, возвращающая вводные данные карты"""
    return ["7000777777777777", "7000777777776666"]


@pytest.fixture
def masked_card_info() -> list[str]:
    """Функция, возвращающая замаскированные данные карты"""
    return ["7000 77** **** 7777", "7000 77** **** 6666"]


@pytest.fixture
def account_info() -> str:
    """Функция, возвращающая вводные данные счета"""
    return "73654108430135872222"


@pytest.fixture
def masked_account_info() -> str:
    """Функция, возвращающая замаскированные данные счета"""
    return "**2222"


@pytest.fixture
def sample_card_data() -> list[tuple[str, str]]:
    """Функция, возвращающая вводные и замаскированные данные карты"""
    return [
        ("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
        ("MasterCard 1111222233334443", "MasterCard 1111 22** **** 4443"),
    ]


@pytest.fixture
def sample_account_data() -> list[tuple[str, str]]:
    """Функция, возвращающая вводные и замаскированные данные счета"""
    return [("Счет 12345678901234567890", "Счет **7890"), ("счет 98765432109876543210", "счет **3210")]


@pytest.fixture
def sample_transactions() -> list[dict[str, Any]]:
    """Фикстура для проверки словарей по state"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "PENDING", "date": "2023-01-02"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03"},
        {"id": 4, "state": "CANCELED", "date": "2023-01-04"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-05"},
    ]
