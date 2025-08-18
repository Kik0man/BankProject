from typing import Any


def filter_by_state(transactions: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Фильтрует список словарей по значению ключа 'state'."""
    result = []
    for word in transactions:
        if word.get("state") == state:
            result.append(word)
    return result


def sort_by_date(transactions: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Сортирует список словарей по дате"""
    return sorted(
        transactions,
        key=lambda x: x["date"],
        reverse=reverse,
    )
