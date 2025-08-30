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


# Фикстуры для теста модуля test_generators
@pytest.fixture
def currency_test_transactions() -> list[dict[str, Any]]:
    """Фикстура для тестов фильтрации по валюте."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]


@pytest.fixture
def empty_transactions_list() -> list[dict[str, Any]]:
    """Фикстура с пустым списком транзакций."""
    return []


@pytest.fixture
def transactions_without_currency_info() -> list[dict[str, Any]]:
    """Фикстура с транзакциями без информации о валюте."""
    return [
        {
            "id": 1,
            "description": "Транзакция без operationAmount",
            "from": "Счет 123",
            "to": "Счет 456"
        },
        {
            "id": 2,
            "operationAmount": {"amount": "100.00"},
            "description": "Транзакция без currency",
            "from": "Счет 123",
            "to": "Счет 456"
        },
        {
            "id": 3,
            "operationAmount": {
                "amount": "200.00",
                "currency": {"name": "USD"}  # Без code
            },
            "description": "Транзакция без code в currency",
            "from": "Счет 123",
            "to": "Счет 456"
        }
    ]


@pytest.fixture
def description_test_transactions() -> list[dict[str, Any]]:
    """Фикстура для тестов извлечения описаний."""
    return [
        {
            "id": 939719570,
            "description": "Перевод организации",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 142264268,
            "description": "Перевод со счета на счет",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 873106923,
            "description": "",  # Пустое описание
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"code": "RUB"}
            }
        },
        {
            "id": 4,  # Без описания
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }
    ]
