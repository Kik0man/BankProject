import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize("user_input, expected", [("7000777777777777", "7000 77** **** 7777"),
                                                  ("7000666655553333", "7000 66** **** 3333")])
def test_get_mask_card_number(user_input, expected):
    assert get_mask_card_number(user_input) == expected


@pytest.mark.parametrize("user_input, expected", [("73654108430135872222", "**2222"),
                                                  ("73654108430135873233", "**3233")])
def test_get_mask_account(user_input, expected):
    assert get_mask_account(user_input) == expected


def test_get_mask_card_number_blank_string():
    with pytest.raises(ValueError):
        get_mask_card_number("")


def test_get_mask_account_blank_string():
    with pytest.raises(ValueError):
        get_mask_account("")


def test_get_mask_card_number_int_type():
    assert get_mask_card_number(5555555566667777) == "5555 55** **** 7777"


def test_get_mask_account_int_type():
    assert get_mask_account(73654108430135873233) == "**3233"


def test_get_mask_account_blank_length():
    with pytest.raises(ValueError):
        get_mask_account(33333333)


def test_get_mask_card_number_blank_length():
    with pytest.raises(ValueError):
        get_mask_card_number(33333333)
