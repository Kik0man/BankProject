import os
import sys
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

from main import get_user_choice, get_user_yes_no

# Добавляем путь к проекту для импорта модулей
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def sample_transaction() -> Dict[str, Any]:
    """Фикстура с тестовой транзакцией для тестирования отображения.

    Returns:
        dict: Тестовая транзакция со всеми необходимыми полями
    """
    return {
        "id": 1,
        "date": "2023-09-05T11:30:32Z",
        "description": "Перевод организации",
        "from": "Счет 58803664561298323391",
        "to": "Счет 39745660563456619397",
        "operationAmount": {"amount": "16210", "currency": {"name": "руб.", "code": "RUB"}},
    }


@pytest.fixture
def sample_card_transaction() -> Dict[str, Any]:
    """Фикстура с тестовой транзакцией с карты.

    Returns:
        dict: Тестовая транзакция с карточными данными
    """
    return {
        "id": 2,
        "date": "2023-07-22T05:02:01Z",
        "description": "Перевод с карты на карту",
        "from": "Visa 1959232722494097",
        "to": "Visa 6804119550473710",
        "operationAmount": {"amount": "30368", "currency": {"name": "USD", "code": "USD"}},
    }


@pytest.fixture
def sample_deposit_transaction() -> Dict[str, Any]:
    """Фикстура с тестовой транзакцией открытия вклада.

    Returns:
        dict: Тестовая транзакция без поля 'from'
    """
    return {
        "id": 3,
        "date": "2023-06-23T19:46:34Z",
        "description": "Открытие вклада",
        "to": "Счет 76768135089446747029",
        "operationAmount": {"amount": "25261", "currency": {"name": "UAH", "code": "UAH"}},
    }


@patch("builtins.input")
def test_get_user_yes_no_yes_variants(mock_input: MagicMock) -> None:
    """Тестирует функцию get_user_yes_no с вариантами ответа 'Да'.

    Args:
        mock_input: Мок функции input
    """
    yes_variants = ["да", "д", "yes", "y"]

    for variant in yes_variants:
        mock_input.return_value = variant
        result = get_user_yes_no("Тестовый вопрос: ")

        assert result is True
        mock_input.assert_called_with("Тестовый вопрос: ")


@patch("builtins.input")
def test_get_user_yes_no_no_variants(mock_input: MagicMock) -> None:
    """Тестирует функцию get_user_yes_no с вариантами ответа 'Нет'.

    Args:
        mock_input: Мок функции input
    """
    no_variants = ["нет", "н", "no", "n"]

    for variant in no_variants:
        mock_input.return_value = variant
        result = get_user_yes_no("Тестовый вопрос: ")

        assert result is False
        mock_input.assert_called_with("Тестовый вопрос: ")


@patch("builtins.input")
@patch("builtins.print")
def test_get_user_yes_no_invalid_then_valid(mock_print: MagicMock, mock_input: MagicMock) -> None:
    """Тестирует обработку неверного ввода в функции get_user_yes_no.

    Args:
        mock_print: Мок функции print
        mock_input: Мок функции input
    """
    mock_input.side_effect = ["неверный", "да"]

    result = get_user_yes_no("Тестовый вопрос: ")

    assert result is True
    assert mock_input.call_count == 2
    mock_print.assert_called_with("Пожалуйста, введите 'Да' или 'Нет'")


@patch("builtins.input")
@patch("builtins.print")
def test_get_user_choice_valid_input(mock_print: MagicMock, mock_input: MagicMock) -> None:
    """Тестирует функцию get_user_choice с корректным вводом.

    Args:
        mock_print: Мок функции print
        mock_input: Мок функции input
    """
    options = ["Опция 1", "Опция 2", "Опция 3"]
    mock_input.return_value = "2"

    result = get_user_choice(options, "Выберите опцию:")

    assert result == "Опция 2"
    # Проверяем что опции были выведены
    assert any("Опция 1" in str(call) for call in mock_print.call_args_list)
    assert any("Опция 2" in str(call) for call in mock_print.call_args_list)
    assert any("Опция 3" in str(call) for call in mock_print.call_args_list)


@patch("builtins.input")
@patch("builtins.print")
def test_get_user_choice_invalid_then_valid(mock_print: MagicMock, mock_input: MagicMock) -> None:
    """Тестирует обработку неверного ввода в функции get_user_choice.

    Args:
        mock_print: Мок функции print
        mock_input: Мок функции input
    """
    options = ["Опция 1", "Опция 2"]
    mock_input.side_effect = ["abc", "5", "1"]

    result = get_user_choice(options, "Выберите опцию:")

    assert result == "Опция 1"
    assert mock_input.call_count == 3
