import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "user_input, expected", [("7000777777777777", "7000 77** **** 7777"), ("7000666655553333", "7000 66** **** 3333")]
)
def test_get_mask_card_number(user_input: str, expected: str) -> None:
    """Тестирование маскировки номера карты с корректными данными."""
    assert get_mask_card_number(user_input) == expected


@pytest.mark.parametrize(
    "user_input, expected", [("73654108430135872222", "**2222"), ("73654108430135873233", "**3233")]
)
def test_get_mask_account(user_input: str, expected: str) -> None:
    """Тестирование маскировки номера счета с корректными данными."""
    assert get_mask_account(user_input) == expected


def test_get_mask_card_number_blank_string() -> None:
    """Тестирование обработки пустой строки в маскировке счета."""
    with pytest.raises(ValueError):
        get_mask_card_number("")


def test_get_mask_account_blank_string() -> None:
    """Тестирование маскировки номера карты с целочисленным входом.
    Проверяет корректное преобразование int в str и последующую маскировку."""
    with pytest.raises(ValueError):
        get_mask_account("")


def test_get_mask_card_number_int_type() -> None:
    """Тестирование маскировки номера карты при передаче целого числа."""
    assert get_mask_card_number(str(5555555566667776)) == "5555 55** **** 7776"


def test_get_mask_account_int_type() -> None:
    """Тестирование маскировки номера счета при передаче целого числа."""
    assert get_mask_account(str(73654108430135873233)) == "**3233"


def test_get_mask_account_blank_length() -> None:
    """Тестирование обработки слишком короткого номера счета."""
    with pytest.raises(ValueError):
        get_mask_account(str(33333333))


def test_get_mask_card_number_blank_length() -> None:
    """Тестирование обработки слишком короткого номера карты."""
    with pytest.raises(ValueError):
        get_mask_card_number(str(33333333))
