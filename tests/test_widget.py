import pytest

from src.widget import mask_account_card, get_date


@pytest.mark.parametrize("input_data, expected", [("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
                                                  ("Счет 12345678901234567890", "Счет **7890"),
                                                  ("Visa Classic 1234567812345678", "Visa Classic 1234 56** **** 5678")])
def test_mask_account_card_valid_input(input_data, expected):
    assert mask_account_card(input_data) == expected


@pytest.mark.parametrize("input_data", ["Visa", "1234567812345678", "", "   ",
                                        "Счет", "Visa 1234","Счет 123",])
def test_mask_account_card_invalid_input(input_data):
    with pytest.raises((ValueError)):
        mask_account_card(input_data)


def test_mask_account_card_mixed_case_account():
    """Тестирование разных регистров для счета"""
    assert mask_account_card("СЧЕТ 12345678901234567890") == "СЧЕТ **7890"
    assert mask_account_card("сЧёТ 12345678901234567890") == "сЧёТ **7890"


@pytest.mark.parametrize("input_data", ["Visa 1234567812345678extra",
                                        "Visa 1234 5678 1234 5678",
                                        "Счет 1234 5678 9012 3456 7890"])
def test_mask_account_card_with_spaces_in_number(input_data):
    result = mask_account_card(input_data)
    assert "**" in result or "****" in result


@pytest.mark.parametrize("input_date, expected", [("2024-03-11T02:26:18.671407", "11.03.2024"),
                                                  ("1998-12-31T23:59:59.999999", "31.12.1998"),
                                                  ("2000-01-01T00:00:00.000000", "01.01.2000"),
                                                  ("2023-02-28T15:30:45.123456", "28.02.2023")])
def test_get_date_valid_formats(input_date, expected):
    assert get_date(input_date) == expected


@pytest.mark.parametrize("invalid_date", [
    "2024-03-11",                      # Без времени
    "2024/03/11T02:26:18",             # Неправильный разделитель даты
    "2024-03-11 02:26:18.671407",      # Пробел вместо T
    "not-a-date",                       # Не дата вообще
    "",                                 # Пустая строка
    "2024-13-45T02:26:18.671407",      # Несуществующая дата
])
def test_get_date_invalid_formats(invalid_date):
    """Тестирование некорректных форматов даты"""
    with pytest.raises((ValueError, IndexError)):
        get_date(invalid_date)


def test_basic_date_conversion():
    result = get_date("2024-03-11T02:26:18.671407")
    assert result == "11.03.2024"


def test_mask_account_card_no_digits():
    with pytest.raises(ValueError, match="Номер должен содержать цифры"):
        mask_account_card("Visa нетцифр")
    with pytest.raises(ValueError, match="Номер должен содержать цифры"):
        mask_account_card("Счет толькотекст")


def test_mask_account_card_no_account_type():
    with pytest.raises(ValueError, match="Не указан тип карты/счета"):
        mask_account_card("1234567812345678")
    with pytest.raises(ValueError, match="Не указан тип карты/счета"):
        mask_account_card("12345678901234567890")


def test_mask_account_card_invalid_account_length():
    with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр"):
        mask_account_card("Счет 1234567890123456789")  # 19 цифр
    with pytest.raises(ValueError, match="Номер счета должен содержать 20 цифр"):
        mask_account_card("Счет 123456789012345678901")  # 21 цифра


def test_mask_account_card_invalid_card_length():
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        mask_account_card("Visa 123456781234567")  # 15 цифр
    with pytest.raises(ValueError, match="Номер карты должен содержать 16 цифр"):
        mask_account_card("Visa 12345678123456789")  # 17 цифр


def test_get_date_invalid_month():
    with pytest.raises(ValueError, match="Некорректный месяц"):
        get_date("2024-00-11T02:26:18.671407")  # месяц 0
    with pytest.raises(ValueError, match="Некорректный месяц"):
        get_date("2024-13-11T02:26:18.671407")  # месяц 13


def test_get_date_invalid_day_general():
    with pytest.raises(ValueError, match="Некорректный день"):
        get_date("2024-03-00T02:26:18.671407")  # день 0
    with pytest.raises(ValueError, match="Некорректный день"):
        get_date("2024-03-32T02:26:18.671407")  # день 32