import json
import os
import tempfile
from typing import Any, Dict, List

from src.utils import load_transactions


def test_load_transactions_valid_file_direct_json_load() -> None:
    """
    Тест загрузки валидного JSON файла с использованием прямого json.load().
    """
    test_data: List[Dict[str, Any]] = [
        {
            "id": 1,
            "date": "2024-01-15",
            "amount": 100.50,
            "currency": "RUB",
            "description": "Purchase in store",
            "status": "completed",
        },
        {
            "id": 2,
            "date": "2024-01-16",
            "amount": 200.75,
            "currency": "USD",
            "description": "Service payment",
            "status": "completed",
        },
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
        temp_file_path: str = f.name

    try:
        # Загружаем транзакции
        result: List[Dict[str, Any]] = load_transactions(temp_file_path)

        # Проверяем результат
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2
        assert result[0]["amount"] == 100.50
        assert result[1]["currency"] == "USD"

    finally:
        os.unlink(temp_file_path)


def test_load_transactions_large_file() -> None:
    """
    Тест загрузки большого JSON файла.
    """
    # Создаем большой список транзакций
    test_data: List[Dict[str, Any]] = []
    for i in range(1000):
        test_data.append({"id": i + 1, "amount": i * 10.0, "currency": "RUB", "description": f"Transaction {i + 1}"})

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f)
        temp_file_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_file_path)
        assert len(result) == 1000
        assert result[999]["id"] == 1000
        assert result[999]["amount"] == 9990.0

    finally:
        os.unlink(temp_file_path)


def test_load_transactions_with_unicode_characters() -> None:
    """
    Тест загрузки файла с Unicode символами.
    """
    test_data: List[Dict[str, Any]] = [
        {
            "id": 1,
            "description": "Покупка в магазине 🛒",  # Русские символы и эмодзи
            "amount": 150.75,
            "currency": "RUB",
            "category": "продукты",
        }
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
        temp_file_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_file_path)
        assert len(result) == 1
        assert result[0]["description"] == "Покупка в магазине 🛒"
        assert result[0]["category"] == "продукты"

    finally:
        os.unlink(temp_file_path)


def test_load_transactions_file_size_zero() -> None:
    """
    Тест загрузки файла с нулевым размером.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        # Создаем пустой файл
        temp_file_path: str = f.name

    try:
        # Убедимся, что файл действительно пустой
        assert os.path.getsize(temp_file_path) == 0

        result: List[Dict[str, Any]] = load_transactions(temp_file_path)
        assert result == []

    finally:
        os.unlink(temp_file_path)


def test_load_transactions_complex_nested_structure() -> None:
    """
    Тест загрузки файла со сложной вложенной структурой.
    """
    test_data: List[Dict[str, Any]] = [
        {
            "id": 1,
            "date": "2024-01-15",
            "amount": 100.50,
            "currency": "RUB",
            "description": "Test transaction",
            "metadata": {
                "location": {"city": "Moscow", "country": "Russia"},
                "device": {"type": "mobile", "os": "iOS"},
            },
            "items": [{"name": "Product A", "price": 50.25}, {"name": "Product B", "price": 50.25}],
        }
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
        temp_file_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_file_path)
        assert len(result) == 1
        assert result[0]["metadata"]["location"]["city"] == "Moscow"
        assert result[0]["metadata"]["device"]["os"] == "iOS"
        assert len(result[0]["items"]) == 2
        assert result[0]["items"][0]["name"] == "Product A"

    finally:
        os.unlink(temp_file_path)
