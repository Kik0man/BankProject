import pytest


@pytest.fixture
def card_info():
    return(['7000777777777777', '7000777777776666 '])


@pytest.fixture
def masked_card_info():
    return(['7000 77** **** 7777', '7000 77** **** 6666'])


@pytest.fixture
def account_info():
    return('73654108430135872222')


@pytest.fixture
def masked_account_info():
    return('**2222')


@pytest.fixture
def sample_card_data():
    return [("Visa 1234567812345678", "Visa 1234 56** **** 5678"),
            ("MasterCard 1111222233334443", "MasterCard 1111 22** **** 4443")]


@pytest.fixture
def sample_account_data():
    return [("Счет 12345678901234567890", "Счет **7890"),
            ("счет 98765432109876543210", "счет **3210")]


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED", "date": "2023-01-01"},
        {"id": 2, "state": "PENDING", "date": "2023-01-02"},
        {"id": 3, "state": "EXECUTED", "date": "2023-01-03"},
        {"id": 4, "state": "CANCELED", "date": "2023-01-04"},
        {"id": 5, "state": "EXECUTED", "date": "2023-01-05"},
    ]