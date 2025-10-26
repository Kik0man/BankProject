import json
import logging
import os
import tempfile

from src.utils import load_transactions, setup_logging_utils


def test_setup_logging_utils() -> None:
    """
    Тестирует настройку логирования для утилит.

    Проверяет, что функция выполняется без ошибок и создается папка logs.
    """
    try:
        setup_logging_utils()
        assert os.path.exists("logs"), "Папка logs должна быть создана"
    finally:
        # Очистка
        if os.path.exists("logs"):
            for handler in logging.getLogger("utils").handlers[:]:
                handler.close()
                logging.getLogger("utils").removeHandler(handler)


def test_load_transactions_valid_file() -> None:
    """
    Тестирует загрузку корректного файла с транзакциями.

    Проверяет, что функция правильно загружает данные из валидного JSON-файла.
    """
    # Создаем временный файл с корректными данными
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        test_data = [
            {"id": 1, "amount": 100, "description": "Test transaction 1"},
            {"id": 2, "amount": 200, "description": "Test transaction 2"},
        ]
        json.dump(test_data, f)
        temp_file_path = f.name

    try:
        result = load_transactions(temp_file_path)

        assert len(result) == 2, "Должно быть загружено 2 транзакции"
        assert result[0]["id"] == 1, "Первая транзакция должна иметь id=1"
        assert result[1]["amount"] == 200, "Вторая транзакция должна иметь amount=200"
    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)


def test_load_transactions_nonexistent_file() -> None:
    """
    Тестирует обработку несуществующего файла.

    Проверяет, что функция возвращает пустой список при попытке загрузить несуществующий файл.
    """
    result = load_transactions("nonexistent_file.json")

    assert result == [], "Для несуществующего файла должен возвращаться пустой список"


def test_load_transactions_empty_file() -> None:
    """
    Тестирует обработку пустого файла.

    Проверяет, что функция возвращает пустой список при загрузке пустого файла.
    """
    # Создаем временный пустой файл
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_file_path = f.name

    try:
        result = load_transactions(temp_file_path)

        assert result == [], "Для пустого файла должен возвращаться пустой список"
    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)


def test_load_transactions_invalid_json() -> None:
    """
    Тестирует обработку файла с некорректным JSON.

    Проверяет, что функция возвращает пустой список при ошибке парсинга JSON.
    """
    # Создаем временный файл с некорректным JSON
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("invalid json content")
        temp_file_path = f.name

    try:
        result = load_transactions(temp_file_path)

        assert result == [], "Для файла с некорректным JSON должен возвращаться пустой список"
    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)


def test_load_transactions_not_list() -> None:
    """
    Тестирует обработку файла с JSON, который не является списком.

    Проверяет, что функция возвращает пустой список, когда данные не являются списком.
    """
    # Создаем временный файл с JSON объектом (не списком)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        test_data = {"id": 1, "amount": 100}  # объект, не список
        json.dump(test_data, f)
        temp_file_path = f.name

    try:
        result = load_transactions(temp_file_path)

        assert result == [], "Для данных не в формате списка должен возвращаться пустой список"
    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)


def test_load_transactions_encoding_issues() -> None:
    """
    Тестирует обработку файла с проблемами кодировки.

    Проверяет, что функция корректно обрабатывает файлы с различными кодировками.
    """
    # Создаем временный файл с корректными данными (кодировка обрабатывается в функции)
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8", delete=False) as f:
        test_data = [{"id": 1, "amount": 100, "description": "Тест с русскими символами"}]
        json.dump(test_data, f, ensure_ascii=False)
        temp_file_path = f.name

    try:
        result = load_transactions(temp_file_path)

        assert len(result) == 1, "Должна быть загружена 1 транзакция"
        assert (
            result[0]["description"] == "Тест с русскими символами"
        ), "Должны корректно обрабатываться русские символы"
    finally:
        # Удаляем временный файл
        os.unlink(temp_file_path)
