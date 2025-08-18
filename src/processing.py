def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Фильтрует список словарей по значению ключа 'state'."""
    result = []
    for word in transactions:
        if word.get("state") == state:
            result.append(word)
    return result
