import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.mark.parametrize("state, expected_count", [
    ("EXECUTED", 3),
    ("PENDING", 1),
    ("CANCELED", 1),
    ("NONEXISTENT", 0),
])
def test_filter_by_state_different_states(sample_transactions, state, expected_count):

    result = filter_by_state(sample_transactions, state)
    assert len(result) == expected_count
    for transaction in result:
        assert transaction["state"] == state


def test_filter_by_state_default_parameter(sample_transactions):
    result = filter_by_state(sample_transactions)
    assert len(result) == 3
    for transaction in result:
        assert transaction["state"] == "EXECUTED"


def test_filter_by_state_no_matching_records(sample_transactions):
    result = filter_by_state(sample_transactions, "COMPLETED")
    assert result == []


def test_filter_by_state_executed():
    data = [
        {"state": "EXECUTED", "id": 1},
        {"state": "PENDING", "id": 2},
        {"state": "EXECUTED", "id": 3}
    ]
    filtered = filter_by_state(data, "EXECUTED")
    assert len(filtered) == 2
    assert filtered[0]["id"] == 1
    assert filtered[1]["id"] == 3


@pytest.mark.parametrize("invalid_date_format", [
    [{"date": ""}],                    # Пустая дата
    [{"date": "not-a-date"}],          # Не дата вообще
    [{"date": "2024/03/11T02:26:18"}], # Неправильный разделитель даты
    [{"date": "2024-13-45"}],          # Несуществующая дата
])
def test_sort_by_date_invalid_formats(invalid_date_format):
    """Тестирование некорректных форматов даты"""
    with pytest.raises(ValueError):
        sort_by_date(invalid_date_format)


@pytest.mark.parametrize("invalid_data", [
    [{"date": None}],
    [{"date": 12345}],
])
def test_sort_by_date_invalid_data_types(invalid_data):
    """Тестирование некорректных типов данных"""
    with pytest.raises(TypeError):
        sort_by_date(invalid_data)


@pytest.mark.parametrize("missing_date_key", [
    [{"id": 1}],                      # Нет ключа 'date'
    [{"id": 1, "date": "2024-03-11T02:26:18"}, {"id": 2}], # Один элемент без даты
])
def test_sort_by_date_missing_key(missing_date_key):
    """Тестирование отсутствия ключа 'date'"""
    with pytest.raises(KeyError):
        sort_by_date(missing_date_key)
