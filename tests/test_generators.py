from typing import Any, Iterator

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


# Тесты для filter_by_currency
def test_filter_usd_transactions(currency_test_transactions: list[dict[str, Any]]) -> None:
    """Тестирование фильтрации USD транзакций. """
    result: list[dict[str, Any]] = list(filter_by_currency(currency_test_transactions, "USD"))

    assert len(result) == 3
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in result)
    expected_ids: list[int] = [939719570, 142264268, 895315941]
    assert [t["id"] for t in result] == expected_ids


def test_filter_rub_transactions(currency_test_transactions: list[dict[str, Any]]) -> None:
    """Тестирование фильтрации RUB транзакций."""
    result: list[dict[str, Any]] = list(filter_by_currency(currency_test_transactions, "RUB"))

    assert len(result) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "RUB" for t in result)
    expected_ids: list[int] = [873106923, 594226727]
    assert [t["id"] for t in result] == expected_ids


def test_filter_eur_transactions_empty(currency_test_transactions: list[dict[str, Any]]) -> None:
    """Тестирование фильтрации по отсутствующей валюте EUR."""
    result: list[dict[str, Any]] = list(filter_by_currency(currency_test_transactions, "EUR"))
    assert result == []


def test_filter_empty_transactions(empty_transactions_list: list[dict[str, Any]]) -> None:
    """Тестирование фильтрации пустого списка."""
    result: list[dict[str, Any]] = list(filter_by_currency(empty_transactions_list, "USD"))
    assert result == []


def test_filter_transactions_without_currency(transactions_without_currency_info: list[dict[str, Any]]) -> None:
    """Тестирование фильтрации транзакций без информации о валюте."""
    result: list[dict[str, Any]] = list(filter_by_currency(transactions_without_currency_info, "USD"))
    assert result == []


def test_currency_filter_generator_behavior(currency_test_transactions: list[dict[str, Any]]) -> None:
    """Тестирование поведения генератора фильтрации по валюте."""
    generator: Iterator[dict[str, Any]] = filter_by_currency(currency_test_transactions, "USD")

    # Первые три USD транзакции
    assert next(generator)["id"] == 939719570
    assert next(generator)["id"] == 142264268
    assert next(generator)["id"] == 895315941

    # Генератор должен завершиться
    with pytest.raises(StopIteration):
        next(generator)


# Тесты для transaction_descriptions
def test_extract_descriptions_from_transactions(currency_test_transactions: list[dict[str, Any]]) -> None:
    """Тестирование извлечения описаний из транзакций."""
    result: list[str] = list(transaction_descriptions(currency_test_transactions))
    expected: list[str] = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert result == expected


def test_descriptions_empty_list(empty_transactions_list: list[dict[str, Any]]) -> None:
    """Тестирование извлечения описаний из пустого списка."""
    result: list[str] = list(transaction_descriptions(empty_transactions_list))
    assert result == []


def test_descriptions_with_missing_and_empty(description_test_transactions: list[dict[str, Any]]) -> None:
    """Тестирование обработки отсутствующих и пустых описаний."""
    result: list[str] = list(transaction_descriptions(description_test_transactions))
    expected: list[str] = ["Перевод организации", "Перевод со счета на счет"]
    assert result == expected


def test_descriptions_generator_behavior(currency_test_transactions: list[dict[str, Any]]) -> None:
    """Тестирование поведения генератора описаний."""
    generator: Iterator[str] = transaction_descriptions(currency_test_transactions)

    # Первые два описания
    assert next(generator) == "Перевод организации"
    assert next(generator) == "Перевод со счета на счет"

    # Пропускаем остальные и проверяем завершение
    for _ in range(3):
        next(generator)

    with pytest.raises(StopIteration):
        next(generator)


# Тесты для card_number_generator
@pytest.mark.parametrize(
    "start,end,expected_first,expected_last,expected_count",
    [
        (1, 5, "0000 0000 0000 0001", "0000 0000 0000 0005", 5),
        (9995, 10000, "0000 0000 0000 9995", "0000 0000 0001 0000", 6),
        (1234567890123456, 1234567890123458, "1234 5678 9012 3456", "1234 5678 9012 3458", 3),
    ],
)
def test_card_number_generation_ranges(
    start: int, end: int, expected_first: str, expected_last: str, expected_count: int
) -> None:
    """Параметризованный тест генерации номеров карт в различных диапазонах."""
    result: list[str] = list(card_number_generator(start, end))

    assert len(result) == expected_count
    assert result[0] == expected_first
    assert result[-1] == expected_last

    # Проверяем формат всех номеров
    for card_number in result:
        assert len(card_number) == 19
        assert card_number.count(" ") == 3
        parts: list[str] = card_number.split(" ")
        assert all(len(part) == 4 and part.isdigit() for part in parts)


def test_card_generator_single_number() -> None:
    """Тестирование генерации одного номера карты."""
    result: list[str] = list(card_number_generator(42, 42))
    assert result == ["0000 0000 0000 0042"]


def test_card_generator_format_validation() -> None:
    """Тестирование валидности формата генерируемых номеров."""
    numbers: list[str] = list(card_number_generator(1234567812345678, 1234567812345680))

    for card_number in numbers:
        assert len(card_number) == 19
        assert card_number[4] == " "
        assert card_number[9] == " "
        assert card_number[14] == " "
        # Проверяем, что все части состоят из цифр
        assert all(part.isdigit() for part in card_number.split(" "))


def test_card_generator_boundary_values() -> None:
    """Тестирование крайних значений генератора."""
    # Минимальное значение
    result: list[str] = list(card_number_generator(1, 1))
    assert result == ["0000 0000 0000 0001"]

    # Максимальное значение
    result = list(card_number_generator(9999999999999999, 9999999999999999))
    assert result == ["9999 9999 9999 9999"]


def test_card_generator_invalid_parameters() -> None:
    """Тестирование обработки невалидных параметров."""
    with pytest.raises(ValueError, match="Начальное значение должно быть не менее 1"):
        list(card_number_generator(0, 5))

    with pytest.raises(ValueError, match="Начальное значение не может быть больше конечного"):
        list(card_number_generator(10, 5))

    with pytest.raises(ValueError, match="Конечное значение не может превышать"):
        list(card_number_generator(1, 10000000000000000))
