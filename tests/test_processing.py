import pytest
from typing import Any, Union
from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected_count",
    [
        ("EXECUTED", 3),
        ("PENDING", 1),
        ("CANCELED", 1),
        ("NONEXISTENT", 0),
    ],
)
def test_filter_by_state_different_states(
    sample_transactions: list[dict[str, Any]], state: str, expected_count: int
) -> None:
    """Тестирование фильтрации транзакций по различным статусам.
    Проверяет, что функция корректно фильтрует транзакции по заданному статусу
    и возвращает правильное количество записей."""

    result = filter_by_state(sample_transactions, state)
    assert len(result) == expected_count
    for transaction in result:
        assert transaction["state"] == state


def test_filter_by_state_default_parameter(sample_transactions: list[dict[str, Any]]) -> None:
    """Тестирование работы функции filter_by_state с параметром по умолчанию.
    Проверяет, что при вызове функции без указания статуса используется
    значение по умолчанию "EXECUTED"."""
    result = filter_by_state(sample_transactions)
    assert len(result) == 3
    for transaction in result:
        assert transaction["state"] == "EXECUTED"


def test_filter_by_state_no_matching_records(sample_transactions: list[dict[str, Any]]) -> None:
    """Тестирование фильтрации при отсутствии записей с указанным статусом.
    Проверяет, что функция возвращает пустой список когда нет транзакций
    с запрошенным статусом."""
    result = filter_by_state(sample_transactions, "COMPLETED")
    assert result == []


def test_filter_by_state_executed() -> None:
    """Тестирование фильтрации по статусу EXECUTED на простых данных.
    Проверяет корректность работы функции на минимальном наборе данных
    и правильность порядка возвращаемых элементов."""
    data = [{"state": "EXECUTED", "id": 1}, {"state": "PENDING", "id": 2}, {"state": "EXECUTED", "id": 3}]
    filtered = filter_by_state(data, "EXECUTED")
    assert len(filtered) == 2
    assert filtered[0]["id"] == 1
    assert filtered[1]["id"] == 3


@pytest.mark.parametrize(
    "invalid_date_format",
    [
        [{"date": ""}],  # Пустая дата
        [{"date": "not-a-date"}],  # Не дата вообще
        [{"date": "2024/03/11T02:26:18"}],  # Неправильный разделитель даты
        [{"date": "2024-13-45"}],  # Несуществующая дата
    ],
)
def test_sort_by_date_invalid_formats(invalid_date_format: list[dict[str, str]]) -> None:
    """Тестирование сортировки с некорректными форматами дат.
    Проверяет, что функция sort_by_date вызывает исключение ValueError
    при попытке сортировки данных с неправильным форматом дат."""
    with pytest.raises(ValueError):
        sort_by_date(invalid_date_format)


@pytest.mark.parametrize(
    "invalid_data",
    [
        [{"date": None}],
        [{"date": 12345}],
    ],
)
def test_sort_by_date_invalid_data_types(invalid_data: list[dict[str, Union[str, None, int]]]) -> None:
    """Тестирование некорректных типов данных"""
    with pytest.raises(TypeError):
        sort_by_date(invalid_data)


@pytest.mark.parametrize(
    "missing_date_key",
    [
        [{"id": 1}],  # Нет ключа 'date'
        [{"id": 1, "date": "2024-03-11T02:26:18"}, {"id": 2}],  # Один элемент без даты
    ],
)
def test_sort_by_date_missing_key(missing_date_key: list[dict[str, Any]]) -> None:
    """Тестирование отсутствия ключа 'date'"""
    with pytest.raises(KeyError):
        sort_by_date(missing_date_key)
