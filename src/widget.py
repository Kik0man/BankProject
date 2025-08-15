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
