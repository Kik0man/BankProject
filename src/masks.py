import logging
import os

logger = logging.getLogger("masks")


def setup_logging_masks() -> None:
    """Настройка логирования для всех модулей"""
    # Создаем папку logs если её нет
    os.makedirs("logs", exist_ok=True)

    # Форматтер для логов
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Обработчик для файла (перезаписывает файл при каждом запуске)
    file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Добавляем обработчик к логгерам
    masks_logger = logging.getLogger("masks")
    masks_logger.setLevel(logging.DEBUG)
    masks_logger.addHandler(file_handler)


def get_mask_card_number(card_numbers: str) -> str:
    """Функция маскирует первые 6 и последние 4 цифры карты пользователя"""
    logger.info(f"Начало маскировки номера карты: {card_numbers}")

    try:
        card_numbers = str(card_numbers)
        # Удаляем все пробелы, если таковые есть
        cleaned_number = card_numbers.replace(" ", "")

        if not cleaned_number.isdigit():
            error_msg = "Номер карты должен содержать только цифры"
            logger.error(f"{error_msg}. Входные данные: {card_numbers}")
            raise ValueError(error_msg)

        # Проверяем длину номера карты
        if len(cleaned_number) != 16:
            error_msg = "Номер карты должен содержать 16 цифр"
            logger.error(f"{error_msg}. Получено цифр: {len(cleaned_number)}")
            raise ValueError(error_msg)

        # Разбиваем номер на части
        masked_number = f"{card_numbers[:4]} {card_numbers[4:6]}** **** {card_numbers[-4:]}"
        logger.info(f"Успешно замаскирован номер карты: {masked_number}")
        return masked_number

    except Exception as e:
        logger.error(f"Ошибка при маскировке номера карты {card_numbers}: {str(e)}")
        raise


def get_mask_account(account_numbers: str) -> str:
    """Функция показывает последние 4 цифры счета пользователя"""
    logger.info(f"Начало маскировки номера счета: {account_numbers}")

    try:
        account_numbers = str(account_numbers)

        # Удаляем все пробелы, если они есть
        cleaned_number = account_numbers.replace(" ", "")
        if not cleaned_number.isdigit():
            error_msg = "Номер счета должен содержать только цифры"
            logger.error(f"{error_msg}. Входные данные: {account_numbers}")
            raise ValueError(error_msg)

        # Проверяем длину номера счета
        if len(cleaned_number) != 20:
            error_msg = "Номер карты должен содержать 20 цифр"
            logger.error(f"{error_msg}. Получено цифр: {len(cleaned_number)}")
            raise ValueError(error_msg)

        masked_account = f"**{cleaned_number[-4:]}"
        logger.info(f"Успешно замаскирован номер счета: {masked_account}")
        return masked_account

    except Exception as e:
        logger.error(f"Ошибка при маскировке номера счета {account_numbers}: {str(e)}")
        raise
