import json
import os
import tempfile
from typing import Any, Dict, List


from src.utils import load_transactions


def test_load_transactions_valid_file() -> None:
    """
    Тест загрузки валидного JSON файла со списком транзакций.
    """
    # Создаем временный файл с валидными данными
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
        # Удаляем временный файл
        os.unlink(temp_file_path)


def test_load_transactions_empty_file() -> None:
    """
    Тест загрузки пустого файла.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        # Создаем пустой файл
        temp_file_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_file_path)
        assert result == []
        assert isinstance(result, list)

    finally:
        os.unlink(temp_file_path)


def test_load_transactions_file_not_found() -> None:
    """
    Тест загрузки несуществующего файла.
    """
    result: List[Dict[str, Any]] = load_transactions("non_existent_file.json")
    assert result == []
    assert isinstance(result, list)


def test_load_transactions_not_list() -> None:
    """
    Тест загрузки файла с данными не в виде списка.
    """
    test_data: Dict[str, Any] = {"transaction": {"id": 1, "amount": 100.50}}

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
        temp_file_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_file_path)
        assert result == []
        assert isinstance(result, list)

    finally:
        os.unlink(temp_file_path)


def test_load_transactions_invalid_json() -> None:
    """
    Тест загрузки файла с некорректным JSON.
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        f.write('{"invalid": json,}')
        temp_file_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_file_path)
        assert result == []
        assert isinstance(result, list)

    finally:
        os.unlink(temp_file_path)


def test_load_transactions_empty_list() -> None:
    """
    Тест загрузки файла с пустым списком.
    """
    test_data: List[Dict[str, Any]] = []

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
        temp_file_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_file_path)
        assert result == []
        assert isinstance(result, list)

    finally:
        os.unlink(temp_file_path)


def test_load_transactions_with_utf8_characters() -> None:
    """
    Тест загрузки файла с UTF-8 символами.
    """
    test_data: List[Dict[str, Any]] = [
        {
            "id": 1,
            "description": "Покупка в магазине",  # Русские символы
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
        assert result[0]["description"] == "Покупка в магазине"
        assert result[0]["category"] == "продукты"

    finally:
        os.unlink(temp_file_path)


def test_load_transactions_complex_structure() -> None:
    """
    Тест загрузки файла со сложной структурой данных.
    """
    test_data: List[Dict[str, Any]] = [
        {
            "id": 1,
            "date": "2024-01-15",
            "amount": 100.50,
            "currency": "RUB",
            "description": "Test transaction",
            "metadata": {"location": "Moscow", "device": "mobile"},
            "tags": ["food", "urgent"],
        }
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
        temp_file_path: str = f.name

    try:
        result: List[Dict[str, Any]] = load_transactions(temp_file_path)
        assert len(result) == 1
        assert "metadata" in result[0]
        assert "tags" in result[0]
        assert result[0]["metadata"]["location"] == "Moscow"
        assert isinstance(result[0]["tags"], list)

    finally:
        os.unlink(temp_file_path)
