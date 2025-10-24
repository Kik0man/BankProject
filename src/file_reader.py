import csv
from typing import Any, Dict, List, cast

import pandas as pd


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из CSV файла

    Args:
        file_path: Путь к CSV файлу
    Raises:
        FileNotFoundError: Если указанный файл не существует
        Exception: При других ошибках чтения файла или обработки данных
    """
    transactions: List[Dict[str, Any]] = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")

            for row in reader:
                # Пропускаем пустые строки
                if not row.get("id") or not row.get("state"):
                    continue

                transaction = {
                    "id": row["id"],
                    "state": row["state"],
                    "date": row["date"],
                    "amount": float(row["amount"]) if row["amount"] else 0.0,
                    "currency_name": row["currency_name"],
                    "currency_code": row["currency_code"],
                    "from": row["from"] if row["from"] else None,
                    "to": row["to"],
                    "description": row["description"],
                }
                transactions.append(transaction)

    except FileNotFoundError:
        raise FileNotFoundError(f"CSV файл не найден: {file_path}")
    except Exception as e:
        raise Exception(f"Ошибка при чтении CSV файла: {str(e)}")

    return transactions


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из Excel файла с использованием pandas

    Args:
        file_path: Путь к Excel файлу (.xlsx, .xls)

    Notes:
        - Функция автоматически обрабатывает пустые ячейки (заменяет NaN на None)
        - Пропускает строки, где отсутствует id или state
        - Автоматически конвертирует поле amount в float
        - Поддерживает форматы .xlsx и .xls
    """
    try:
        # Читаем Excel файл
        df: pd.DataFrame = pd.read_excel(file_path)

        # Заменяем NaN на None
        df = df.replace({pd.NA: None, pd.NaT: None})
        df = df.where(pd.notnull(df), None)

        # Конвертируем в список словарей и явно указываем тип
        raw_transactions = df.to_dict("records")
        transactions: List[Dict[str, Any]] = cast(List[Dict[str, Any]], raw_transactions)

        # Фильтруем пустые строки и конвертируем amount
        filtered_transactions: List[Dict[str, Any]] = []
        for transaction in transactions:
            if transaction.get("id") and transaction.get("state"):
                # Конвертируем amount в float если нужно
                if "amount" in transaction and transaction["amount"] is not None:
                    if isinstance(transaction["amount"], str):
                        transaction["amount"] = float(transaction["amount"])
                    elif isinstance(transaction["amount"], (int, float)):
                        transaction["amount"] = float(transaction["amount"])
                filtered_transactions.append(transaction)

        return filtered_transactions

    except FileNotFoundError:
        raise FileNotFoundError(f"Excel файл не найден: {file_path}")
    except Exception as e:
        raise Exception(f"Ошибка при чтении Excel файла: {str(e)}")