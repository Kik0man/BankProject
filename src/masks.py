def get_mask_card_number(card_numbers: str) -> str:
    """Функция маскирует первые 6 и последние 4 цифры карты пользователя"""

    # Удаляем все пробелы, если они есть
    cleaned_number = card_numbers.replace(" ", "")
    if not cleaned_number.isdigit():
        raise ValueError("Номер карты должен содержать только цифры")

    # Проверяем длину номера карты
    if len(cleaned_number) != 16:
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Разбиваем номер на части
    first_part = cleaned_number[:6]
    last_part = cleaned_number[-4:]
    return f"{first_part[:4]} {first_part[4:6]}** **** {last_part}"


def get_mask_account(account_numbers: str) -> str:
    """Функция показывает последние 4 цифры счета пользователя"""

    # Удаляем все пробелы, если они есть
    cleaned_number = account_numbers.replace(" ", "")
    if not cleaned_number.isdigit():
        raise ValueError("Номер счета должен содержать только цифры")

    # Проверяем длину номера счета
    if len(cleaned_number) != 20:
        raise ValueError("Номер карты должен содержать 20 цифр")

    return f"**{cleaned_number[-4:]}"
