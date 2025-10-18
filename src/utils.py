import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает финансовые транзакции из JSON-файла.
    Args: file_path - Путь до JSON-файла с транзакциями"""
    try:
        # Проверяем существование файла по указанному пути
        if not os.path.exists(file_path):
            return []

        # Открываем файл для чтения с кодировкой UTF-8
        with open(file_path, "r", encoding="utf-8") as file:
            # Читаем содержимое файла
            content = file.read().strip()

            # Проверяем, не пустой ли файл
            if not content:
                return []

            # Парсим JSON содержимое
            data = json.loads(content)

            # Проверяем, что полученные данные являются списком
            if isinstance(data, list):
                return data
            else:
                return []

    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        # Обрабатываем ошибки: некорректный JSON, файл не найден, нет прав доступа
        return []
