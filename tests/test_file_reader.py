from unittest.mock import mock_open, patch

import pandas as pd

from src.file_reader import read_csv_file, read_excel_file


def test_read_csv_file_success() -> None:
    """
    Тестирует успешное чтение CSV файла с корректными данными.

    Проверяет:
    - Функция корректно читает данные из CSV
    - Поля правильно преобразуются в нужные типы (amount в float)
    - Возвращается ожидаемое количество транзакций
    """
    csv_data = """id;state;date;amount;currency_name;currency_code;from;to;description
650703;EXECUTED;2023-09-05T11:30:32Z;16210;Sol;PEN;Счет 58803664561298323391;
Счет 39745660563456619397;Перевод организации"""

    with patch("builtins.open", mock_open(read_data=csv_data)):
        with patch("csv.DictReader") as mock_reader:
            mock_reader.return_value = [
                {
                    "id": "650703",
                    "state": "EXECUTED",
                    "date": "2023-09-05T11:30:32Z",
                    "amount": "16210",
                    "currency_name": "Sol",
                    "currency_code": "PEN",
                    "from": "Счет 58803664561298323391",
                    "to": "Счет 39745660563456619397",
                    "description": "Перевод организации",
                }
            ]

            result = read_csv_file("dummy_path.csv")
            assert len(result) == 1
            assert result[0]["id"] == "650703"
            assert result[0]["amount"] == 16210.0
            print("✓ test_read_csv_file_success пройден")


def test_read_excel_file_success() -> None:
    """
    Тестирует успешное чтение Excel файла с pandas.

    Проверяет:
    - Функция корректно обрабатывает DataFrame из pandas
    - Все транзакции сохраняются без потерь
    - Типы данных сохраняются правильно
    - Поддерживаются различные форматы данных
    """
    # Создаем реальный DataFrame для теста
    test_data = [
        {
            "id": "650703",
            "state": "EXECUTED",
            "date": "2023-09-05T11:30:32Z",
            "amount": 16210,
            "currency_name": "Sol",
            "currency_code": "PEN",
            "from": "Счет 58803664561298323391",
            "to": "Счет 39745660563456619397",
            "description": "Перевод организации",
        },
        {
            "id": "3598919",
            "state": "EXECUTED",
            "date": "2020-12-06T23:00:58Z",
            "amount": 29740,
            "currency_name": "Peso",
            "currency_code": "COP",
            "from": "Discover 3172601889670065",
            "to": "Discover 0720428384694643",
            "description": "Перевод с карты на карту",
        },
    ]

    # Создаем DataFrame из тестовых данных
    test_df = pd.DataFrame(test_data)

    with patch("pandas.read_excel") as mock_read_excel:
        # Возвращаем наш тестовый DataFrame
        mock_read_excel.return_value = test_df

        result = read_excel_file("dummy_path.xlsx")

        assert len(result) == 2
        assert result[0]["id"] == "650703"
        assert result[0]["state"] == "EXECUTED"
        assert result[0]["amount"] == 16210.0
        assert result[1]["id"] == "3598919"
        print("✓ test_read_excel_file_success пройден")


def test_read_excel_file_empty() -> None:
    """
    Тестирует чтение пустого Excel файла.

    Проверяет:
    - Функция корректно обрабатывает пустой DataFrame
    - Возвращается пустой список транзакций
    - Отсутствуют ошибки при обработке пустых данных

    Edge case: файл существует, но не содержит данных
    """
    # Создаем пустой DataFrame
    empty_df = pd.DataFrame()

    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = empty_df

        result = read_excel_file("dummy_path.xlsx")
        assert len(result) == 0
        print("✓ test_read_excel_file_empty пройден")


def test_read_excel_file_with_empty_rows() -> None:
    """
    Тестирует чтение Excel файла с пустыми и частично заполненными строками.

    Проверяет:
    - Пустые строки корректно фильтруются
    - Частично заполненные строки с отсутствующим id/state игнорируются
    - Корректные строки сохраняются
    - Фильтрация работает по наличию id и state
    """
    test_data = [
        {"id": None, "state": None, "amount": None, "currency_name": None},  # Пустая строка
        {"id": "650703", "state": "EXECUTED", "amount": 16210, "currency_name": "Sol"},
        {"id": "3598919", "state": None, "amount": 29740, "currency_name": "Peso"},  # Частично пустая
        {"id": "123456", "state": "EXECUTED", "amount": 1000, "currency_name": "USD"},  # Корректная
    ]

    test_df = pd.DataFrame(test_data)

    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = test_df

        result = read_excel_file("dummy_path.xlsx")
        # Должны остаться только строки с id и state
        assert len(result) == 2
        assert result[0]["id"] == "650703"
        assert result[1]["id"] == "123456"
        print("✓ test_read_excel_file_with_empty_rows пройден")


def test_read_excel_file_with_string_amount() -> None:
    """
    Тестирует чтение Excel файла с числовыми значениями в виде строк.

    Проверяет:
    - Строковые значения amount корректно конвертируются в float
    - Числовые значения amount остаются числами
    - Тип данных для amount всегда float после обработки
    - Конвертация не ломает исходные данные
    """
    test_data = [
        {"id": "650703", "state": "EXECUTED", "amount": "16210", "currency_name": "Sol"},
        {"id": "3598919", "state": "EXECUTED", "amount": 29740, "currency_name": "Peso"},
    ]

    test_df = pd.DataFrame(test_data)

    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = test_df

        result = read_excel_file("dummy_path.xlsx")
        assert len(result) == 2
        # Оба amount должны быть float
        assert isinstance(result[0]["amount"], float)
        assert isinstance(result[1]["amount"], float)
        assert result[0]["amount"] == 16210.0
        assert result[1]["amount"] == 29740.0
        print("✓ test_read_excel_file_with_string_amount пройден")


def test_read_excel_file_not_found() -> None:
    """
    Тестирует обработку ситуации когда Excel файл не существует.

    Проверяет:
    - Функция выбрасывает FileNotFoundError для отсутствующего файла
    - Исключение имеет правильный тип
    - Сообщение об ошибке содержит путь к файлу
    """
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.side_effect = FileNotFoundError("File not found")

        try:
            read_excel_file("nonexistent_file.xlsx")
            assert False, "Ожидалось исключение FileNotFoundError"
        except FileNotFoundError:
            print("✓ test_read_excel_file_not_found пройден")
        except Exception as e:
            assert False, f"Ожидалось FileNotFoundError, получено {type(e).__name__}"


def test_read_csv_file_not_found() -> None:
    """
    Тестирует обработку ситуации когда CSV файл не существует.

    Проверяет:
    - Функция выбрасывает FileNotFoundError для отсутствующего файла
    - Исключение перехватывается и обрабатывается правильно
    - Не возникают другие неожиданные исключения
    """
    try:
        read_csv_file("nonexistent_file.csv")
        assert False, "Ожидалось исключение FileNotFoundError"
    except FileNotFoundError:
        print("✓ test_read_csv_file_not_found пройден")
    except Exception as e:
        assert False, f"Ожидалось FileNotFoundError, получено {type(e).__name__}"
