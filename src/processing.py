import re
from collections import Counter
from datetime import datetime
from typing import Any


def filter_by_state(transactions: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    result = []
    for word in transactions:
        if word.get("state") == state:
            result.append(word)
    return result


def sort_by_date(transactions: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Сортирует список словарей по дате, в зависимости от значения reverse, по умолчанию True"""
    # Проверяем наличие ключа 'date' во всех элементах

    for transaction in transactions:
        if "date" not in transaction:
            raise KeyError("Отсутствует ключ 'date'")

        date_str = transaction["date"]
        if not isinstance(date_str, str):
            raise TypeError(f"Дата должна быть строкой, получено: {type(date_str)}")

        # Базовая проверка формата - должна содержать хотя бы год-месяц-день
        if not (len(date_str) >= 10 and date_str.count("-") >= 2):
            raise ValueError(f"Некорректный формат даты: {date_str}")

    # Сортируем с обработкой ошибок парсинга
    try:
        return sorted(
            transactions, key=lambda x: datetime.fromisoformat(x["date"].replace("Z", "+00:00")), reverse=reverse
        )
    except ValueError as e:
        raise ValueError(f"Некорректный формат даты: {e}")


def filter_by_description(transactions: list[dict[str, Any]], search_string: str) -> list[dict[str, Any]]:
    """
    Фильтрует транзакции по строке поиска в описании с использованием регулярных выражений.

    Args:
        transactions: Список словарей с транзакциями
        search_string: Строка для поиска в описании
    """
    if not search_string:
        return transactions

    filtered_transactions = []
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)

    for transaction in transactions:
        description = transaction.get("description", "")
        if pattern.search(str(description)):
            filtered_transactions.append(transaction)

    return filtered_transactions


def count_transactions_by_category(transactions: list[dict[str, Any]], categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество операций по категориям.

    Args:
        transactions: Список словарей с транзакциями
        categories: Список категорий для подсчета
    """

    # Собираем все описания
    descriptions = []
    for transaction in transactions:
        description = transaction.get("description", "")
        if description:
            descriptions.append(description.lower())

    # Используем Counter для подсчета
    description_counter = Counter(descriptions)

    # Формируем результат только для запрошенных категорий
    result = {}
    for category in categories:
        category_lower = category.lower()
        result[category] = description_counter.get(category_lower, 0)

    return result
