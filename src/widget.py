from mask import get_mask_account, get_mask_card_number


def mask_account_card(full_bank_info: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа.
    Формат ввода: 'Тип Номер'"""

    # Разделяем строку на тип и номер по пробелам
    words = full_bank_info.split()

    # Присваиваем значения после разделения
    account_type = " ".join(words[:-1])
    number = words[-1]

    # Определяем тип и применяем соответствующую маскировку
    if "счет" in account_type.lower():
        return f"{account_type} {get_mask_account(number)}"
    else:
        return f"{account_type} {get_mask_card_number(number)}"


def get_date(date_str: str) -> str:
    """Преобразует дату из формата "ГГГГ-ММ-ДДTЧЧ:ММ:СС.микросекунды" в "ДД.ММ.ГГГГ" """
    # 1. Разделяем дату и время
    date_time_parts = date_str.split("T")
    date_part = date_time_parts[0]

    # 2. Разбиваем дату на компоненты
    date_components = date_part.split("-")

    # 3. Извлекаем отдельные компоненты
    year = date_components[0]
    month = date_components[1]
    day = date_components[2]

    return f"{day}.{month}.{year}"
