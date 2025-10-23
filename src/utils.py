import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает финансовые транзакции из JSON-файла.
    Args:
        file_path: Путь до JSON-файла с транзакциями
    """
    try:
        # Проверяем существование файла по указанному пути
        if not os.path.exists(file_path):
            return []

        # Получаем размер файла для проверки на пустоту
        if os.path.getsize(file_path) == 0:
            return []

        # Открываем файл и передаем файловый объект в json.load()
        with open(file_path, "r", encoding="utf-8") as file:
            # Используем json.load() для чтения из файлового объекта
            data = json.load(file)

            # Проверяем, что полученные данные являются списком
            if isinstance(data, list):
                return data
            else:
                return []

    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        # Обрабатываем ошибки: некорректный JSON, файл не найден, нет прав доступа
        return []
    except Exception:
        # Обрабатываем любые другие ошибки
        return []
