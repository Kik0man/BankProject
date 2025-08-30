from typing import Any, Generator, Iterator, Optional


def filter_by_currency(
    transactions: list[dict[str, Any]],
    currency_code: str = "USD"
) -> Iterator[Optional[dict[str, Any]]]:
    """Фильтрует транзакции по валюте операции.
    Args:
    transactions: список словарей с транзакциями
    currency_code: код валюты для фильтрации (например, "USD")"""
    for transaction in transactions:
        # Проверяем, что транзакция имеет информацию о валюте
        if (
            "operationAmount" in transaction
            and "currency" in transaction["operationAmount"]
            and "code" in transaction["operationAmount"]["currency"]
        ):
            # Сравниваем код валюты с заданным
            if transaction["operationAmount"]["currency"]["code"] == currency_code:
                yield transaction


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Generator[str, None, None]:
    """Генератор, который возвращает описание каждой операции из списка транзакций.
    Пропускает транзакции без описания."""
    for transaction in transactions:
        try:
            if isinstance(transaction, dict) and "description" in transaction:
                description = transaction["description"]
                if isinstance(description, str) and description.strip():
                    yield description
        except (AttributeError, TypeError, KeyError):
            continue


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Генератор номеров банковских карт в заданном диапазоне."""
    # 1. Проверяем корректность входных параметров
    if start < 1:
        raise ValueError("Начальное значение должно быть не менее 1")
    if end > 9999999999999999:
        raise ValueError("Конечное значение не может превышать 9999999999999999")
    if start > end:
        raise ValueError("Начальное значение не может быть больше конечного")

    # 2. Перебираем все номера в заданном диапазоне
    for number in range(start, end + 1):
        # 3. Преобразуем число в строку и заполняем нулями слева до 16 цифр
        card_str = str(number).zfill(16)
        # 4. Форматируем строку: разбиваем на группы по 4 цифры с пробелами
        formatted_card = f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"
        # 5. Возвращаем отформатированный номер карты
        yield formatted_card
