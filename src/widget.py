from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(full_bank_info: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа."""

    # Извлекаем все цифры
    all_digits = "".join(char for char in full_bank_info if char.isdigit())

    if not all_digits:
        raise ValueError("Номер должен содержать цифры")

    # Извлекаем тип: удаляем цифры, но сохраняем все остальные символы
    account_type = ""
    for char in full_bank_info:
        if not char.isdigit():
            account_type += char
    account_type = account_type.strip()

    if not account_type:
        raise ValueError("Не указан тип карты/счета")

    # Определяем тип
    if "счет" in account_type.lower() or "счёт" in account_type.lower():
        if len(all_digits) != 20:
            raise ValueError("Номер счета должен содержать 20 цифр")
        return f"{account_type} {get_mask_account(all_digits)}"
    else:
        if len(all_digits) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")
        return f"{account_type} {get_mask_card_number(all_digits)}"


def get_date(date_str: str) -> str:
    """Преобразует дату из формата "ГГГГ-ММ-ДДTЧЧ:ММ:СС.микросекунды" в "ДД.ММ.ГГГГ" """

    # Базовые проверки
    if not date_str or "T" not in date_str:
        raise ValueError("Неверный формат даты")

    # Разделяем дату и время
    try:
        date_part = date_str.split("T")[0]
    except IndexError:
        raise ValueError("Неверный формат даты")

    # Разбиваем дату на компоненты
    try:
        year, month, day = date_part.split("-")
    except ValueError:
        raise ValueError("Неверный формат даты. Ожидается ГГГГ-ММ-ДД")

    # Проверяем что это числа
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        raise ValueError("Компоненты даты должны быть числами")

    # Проверяем валидность даты
    year_int = int(year)
    month_int = int(month)
    day_int = int(day)

    # Проверка месяца
    if month_int < 1 or month_int > 12:
        raise ValueError("Некорректный месяц")

    # Проверка дня
    if day_int < 1 or day_int > 31:
        raise ValueError("Некорректный день")

    # Дополнительные проверки для конкретных месяцев
    if month_int in [4, 6, 9, 11] and day_int > 30:  # Апрель, Июнь, Сентябрь, Ноябрь
        raise ValueError("Некорректный день для этого месяца")

    if month_int == 2:  # Февраль
        # Упрощенная проверка високосного года
        is_leap = (year_int % 4 == 0 and year_int % 100 != 0) or (year_int % 400 == 0)
        if (is_leap and day_int > 29) or (not is_leap and day_int > 28):
            raise ValueError("Некорректный день для февраля")

    return f"{day}.{month}.{year}"
