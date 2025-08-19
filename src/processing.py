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
    """Сортирует список словарей по дате, в зависимости от значения reverse"""

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
