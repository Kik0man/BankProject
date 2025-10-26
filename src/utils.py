import json
import logging
import os
from typing import Any, Dict, List

logger = logging.getLogger("utils")


def setup_logging_utils() -> None:
    """Настройка логирования для всех модулей"""
    # Создаем папку logs если её нет
    os.makedirs("logs", exist_ok=True)

    # Форматтер для логов
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Обработчик для файла (перезаписывает файл при каждом запуске)
    file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгерам
    utils_logger = logging.getLogger("utils")
    utils_logger.setLevel(logging.DEBUG)
    utils_logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает финансовые транзакции из JSON-файла.
    Args:
        file_path: Путь до JSON-файла с транзакциями
    """
    logger.info(f"Начало загрузки транзакций из файла: {file_path}")

    try:
        # Проверяем существование файла по указанному пути
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        # Получаем размер файла для проверки на пустоту
        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл пуст: {file_path}")
            return []

        # Открываем файл и передаем файловый объект в json.load()
        with open(file_path, "r", encoding="utf-8") as file:
            # Используем json.load() для чтения из файлового объекта
            data = json.load(file)
            logger.info(f"Успешно загружено {len(data) if isinstance(data, list) else 0} транзакций")

            # Проверяем, что полученные данные являются списком
            if isinstance(data, list):
                return data
            else:
                logger.warning("Данные в файле не являются списком")
                return []

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {str(e)}")
        return []
    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {file_path} - {str(e)}")
        return []
    except PermissionError as e:
        logger.error(f"Нет прав доступа к файлу: {file_path} - {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при загрузке файла {file_path}: {str(e)}")
        return []
