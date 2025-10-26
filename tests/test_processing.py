from typing import Any, Union

import pytest

from src.processing import count_transactions_by_category, filter_by_description, filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions_with_descriptions() -> list[dict[str, Any]]:
    """Фикстура с тестовыми транзакциями для тестирования фильтрации по описанию.

    Returns:
        list[dict]: Список тестовых транзакций с разными описаниями
    """
    return [
        {
            "id": 1,
            "description": "Перевод организации",
            "date": "2023-01-01T00:00:00Z",
            "state": "EXECUTED",
            "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
        },
        {
            "id": 2,
            "description": "Открытие вклада",
            "date": "2023-01-02T00:00:00Z",
            "state": "EXECUTED",
            "operationAmount": {"amount": "200", "currency": {"code": "USD"}},
        },
        {
            "id": 3,
            "description": "Перевод с карты на карту",
            "date": "2023-01-03T00:00:00Z",
            "state": "PENDING",
            "operationAmount": {"amount": "300", "currency": {"code": "EUR"}},
        },
        {
            "id": 4,
            "description": "Перевод организации",
            "date": "2023-01-04T00:00:00Z",
            "state": "EXECUTED",
            "operationAmount": {"amount": "400", "currency": {"code": "RUB"}},
        },
        {
            "id": 5,
            "description": "Перевод со счета на счет",
            "date": "2023-01-05T00:00:00Z",
            "state": "CANCELED",
            "operationAmount": {"amount": "500", "currency": {"code": "GBP"}},
        },
    ]


@pytest.fixture
def sample_transactions_for_categories() -> list[dict[str, Any]]:
    """Фикстура с транзакциями для тестирования подсчета по категориям.

    Returns:
        list[dict]: Список транзакций с разными категориями и повторениями
    """
    return [
        {"id": 1, "description": "Перевод организации", "state": "EXECUTED", "amount": 100},
        {"id": 2, "description": "Открытие вклада", "state": "EXECUTED", "amount": 200},
        {"id": 3, "description": "Перевод с карты на карту", "state": "PENDING", "amount": 300},
        {"id": 4, "description": "Перевод организации", "state": "EXECUTED", "amount": 400},
        {"id": 5, "description": "Открытие вклада", "state": "CANCELED", "amount": 500},
        {"id": 6, "description": "Перевод организации", "state": "EXECUTED", "amount": 600},
        {"id": 7, "description": "Перевод со счета на счет", "state": "EXECUTED", "amount": 700},
    ]


def test_filter_by_description_existing_word(sample_transactions_with_descriptions: list[dict[str, Any]]) -> None:
    """Тестирует фильтрацию транзакций по существующему слову в описании.

    Args:
        sample_transactions_with_descriptions: Фикстура с тестовыми транзакциями

    Checks:
        - Возвращает правильное количество транзакций
        - Все возвращенные транзакции содержат искомое слово
        - Сохраняется порядок исходных транзакций
    """
    result = filter_by_description(sample_transactions_with_descriptions, "организации")

    assert len(result) == 2
    assert all("организации" in transaction["description"].lower() for transaction in result)
    assert result[0]["id"] == 1
    assert result[1]["id"] == 4


def test_filter_by_description_case_insensitive(sample_transactions_with_descriptions: list[dict[str, Any]]) -> None:
    """Тестирует регистронезависимый поиск в описаниях транзакций.

    Args:
        sample_transactions_with_descriptions: Фикстура с тестовыми транзакциями

    Checks:
        - Поиск работает независимо от регистра
        - Результаты одинаковы для разных вариантов регистра
    """
    result_upper = filter_by_description(sample_transactions_with_descriptions, "ПЕРЕВОД")
    result_lower = filter_by_description(sample_transactions_with_descriptions, "перевод")
    result_mixed = filter_by_description(sample_transactions_with_descriptions, "ПеРеВоД")

    assert len(result_upper) == 4
    assert len(result_lower) == 4
    assert len(result_mixed) == 4
    assert result_upper == result_lower == result_mixed


def test_filter_by_description_nonexistent_word(sample_transactions_with_descriptions: list[dict[str, Any]]) -> None:
    """Тестирует фильтрацию по несуществующему слову в описаниях.

    Args:
        sample_transactions_with_descriptions: Фикстура с тестовыми транзакциями

    Checks:
        - Возвращает пустой список при отсутствии совпадений
    """
    result = filter_by_description(sample_transactions_with_descriptions, "несуществующееслово")

    assert len(result) == 0
    assert result == []


def test_filter_by_description_empty_string(sample_transactions_with_descriptions: list[dict[str, Any]]) -> None:
    """Тестирует фильтрацию по пустой строке поиска.

    Args:
        sample_transactions_with_descriptions: Фикстура с тестовыми транзакциями

    Checks:
        - Возвращает все транзакции при пустой строке поиска
    """
    result = filter_by_description(sample_transactions_with_descriptions, "")

    assert len(result) == len(sample_transactions_with_descriptions)
    assert result == sample_transactions_with_descriptions


def test_filter_by_description_partial_word(sample_transactions_with_descriptions: list[dict[str, Any]]) -> None:
    """Тестирует фильтрацию по части слова в описании.

    Args:
        sample_transactions_with_descriptions: Фикстура с тестовыми транзакциями

    Checks:
        - Находит транзакции по части слова
        - Корректно работает с подстроками
    """
    result = filter_by_description(sample_transactions_with_descriptions, "вод")

    assert len(result) == 4
    assert all("перевод" in transaction["description"].lower() for transaction in result)


def test_filter_by_description_special_characters(sample_transactions_with_descriptions: list[dict[str, Any]]) -> None:
    """Тестирует фильтрацию с использованием специальных символов.

    Args:
        sample_transactions_with_descriptions: Фикстура с тестовыми транзакциями

    Checks:
        - Корректно экранирует специальные символы в регулярных выражениях
    """
    result = filter_by_description(sample_transactions_with_descriptions, ".")

    # Точка должна быть проэкранирована и не работать как спецсимвол
    assert len(result) == 0


def test_filter_by_description_without_description_field() -> None:
    """Тестирует фильтрацию транзакций без поля description.

    Checks:
        - Корректно обрабатывает транзакции без поля description
        - Не вызывает исключений при отсутствии поля
    """
    transactions_without_desc: list[dict[str, Any]] = [
        {"id": 1, "date": "2023-01-01T00:00:00Z"},
        {"id": 2, "description": "", "date": "2023-01-02T00:00:00Z"},
        {"id": 3, "description": None, "date": "2023-01-03T00:00:00Z"},
    ]

    result = filter_by_description(transactions_without_desc, "перевод")

    assert len(result) == 0
    assert result == []


def test_count_transactions_by_category_existing_categories(
    sample_transactions_for_categories: list[dict[str, Any]],
) -> None:
    """Тестирует подсчет транзакций по существующим категориям.

    Args:
        sample_transactions_for_categories: Фикстура с транзакциями для подсчета

    Checks:
        - Возвращает правильное количество для каждой категории
        - Учитывает все вхождения категорий
    """
    categories = ["Перевод организации", "Открытие вклада", "Перевод с карты на карту"]
    result = count_transactions_by_category(sample_transactions_for_categories, categories)

    assert result["Перевод организации"] == 3
    assert result["Открытие вклада"] == 2
    assert result["Перевод с карты на карту"] == 1


def test_count_transactions_by_category_case_insensitive(
    sample_transactions_for_categories: list[dict[str, Any]],
) -> None:
    """Тестирует регистронезависимый подсчет транзакций по категориям.

    Args:
        sample_transactions_for_categories: Фикстура с транзакциями для подсчета

    Checks:
        - Подсчет работает независимо от регистра категорий
    """
    categories_upper = ["ПЕРЕВОД ОРГАНИЗАЦИИ", "ОТКРЫТИЕ ВКЛАДА"]
    categories_lower = ["перевод организации", "открытие вклада"]

    result_upper = count_transactions_by_category(sample_transactions_for_categories, categories_upper)
    result_lower = count_transactions_by_category(sample_transactions_for_categories, categories_lower)

    assert result_upper["ПЕРЕВОД ОРГАНИЗАЦИИ"] == 3
    assert result_lower["перевод организации"] == 3
    assert result_upper["ОТКРЫТИЕ ВКЛАДА"] == 2
    assert result_lower["открытие вклада"] == 2


def test_count_transactions_by_category_nonexistent_categories(
    sample_transactions_for_categories: list[dict[str, Any]],
) -> None:
    """Тестирует подсчет транзакций по несуществующим категориям.

    Args:
        sample_transactions_for_categories: Фикстура с транзакциями для подсчета

    Checks:
        - Возвращает 0 для несуществующих категорий
    """
    categories = ["Несуществующая категория", "Другая категория"]
    result = count_transactions_by_category(sample_transactions_for_categories, categories)

    assert result["Несуществующая категория"] == 0
    assert result["Другая категория"] == 0


def test_count_transactions_by_category_mixed_categories(
    sample_transactions_for_categories: list[dict[str, Any]],
) -> None:
    """Тестирует подсчет транзакций по смеси существующих и несуществующих категорий.

    Args:
        sample_transactions_for_categories: Фикстура с транзакциями для подсчета

    Checks:
        - Корректно обрабатывает смешанный список категорий
    """
    categories = ["Перевод организации", "Несуществующая категория", "Открытие вклада"]
    result = count_transactions_by_category(sample_transactions_for_categories, categories)

    assert result["Перевод организации"] == 3
    assert result["Несуществующая категория"] == 0
    assert result["Открытие вклада"] == 2


def test_count_transactions_by_category_empty_categories(
    sample_transactions_for_categories: list[dict[str, Any]],
) -> None:
    """Тестирует подсчет транзакций по пустому списку категорий.

    Args:
        sample_transactions_for_categories: Фикстура с транзакциями для подсчета

    Checks:
        - Возвращает пустой словарь при пустом списке категорий
    """
    result = count_transactions_by_category(sample_transactions_for_categories, [])

    assert result == {}


def test_count_transactions_by_category_empty_transactions() -> None:
    """Тестирует подсчет транзакций по пустому списку транзакций.

    Checks:
        - Корректно обрабатывает пустой список транзакций
        - Возвращает 0 для всех категорий
    """
    categories = ["Перевод организации", "Открытие вклада"]
    result = count_transactions_by_category([], categories)

    assert result["Перевод организации"] == 0
    assert result["Открытие вклада"] == 0


def test_count_transactions_by_category_transactions_without_description() -> None:
    """Тестирует подсчет транзакций без поля description.

    Checks:
        - Корректно обрабатывает транзакции без поля description
        - Не вызывает исключений
    """
    transactions_without_desc: list[dict[str, Any]] = [
        {"id": 1, "amount": 100},
        {"id": 2, "description": "", "amount": 200},
        {"id": 3, "description": None, "amount": 300},
    ]

    categories = ["Перевод организации"]
    result = count_transactions_by_category(transactions_without_desc, categories)

    assert result["Перевод организации"] == 0


# Существующие тесты остаются без изменений
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
    data: list[dict[str, Any]] = [
        {"state": "EXECUTED", "id": 1},
        {"state": "PENDING", "id": 2},
        {"state": "EXECUTED", "id": 3},
    ]
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
