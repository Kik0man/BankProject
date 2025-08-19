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


