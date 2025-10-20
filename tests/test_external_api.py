from typing import Any, Dict
from unittest.mock import Mock, patch


from src.external_api import convert_currency_apilayer, get_amount_in_rubles


def test_get_amount_in_rubles_rub_currency() -> None:
    """
    Тест для RUB транзакции с реальной структурой из operations.json.
    """
    transaction: Dict[str, Any] = {
        "id": 441945886,
        "state": "EXECUTED",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
    }

    result = get_amount_in_rubles(transaction)

    assert result == 31957.58
    assert isinstance(result, float)


def test_get_amount_in_rubles_usd_currency() -> None:
    """
    Тест для USD транзакции с реальной структурой из operations.json.
    """
    transaction: Dict[str, Any] = {
        "id": 41428829,
        "state": "EXECUTED",
        "operationAmount": {"amount": "100.0", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
    }

    # Мокаем API запрос
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"RUB": 91.45}}
        mock_get.return_value = mock_response

        result = get_amount_in_rubles(transaction)

        # 100 USD * 91.45 = 9145 RUB
        assert result == 9145.0
        assert isinstance(result, float)


def test_get_amount_in_rubles_eur_currency() -> None:
    """
    Тест для EUR транзакции с реальной структурой из operations.json.
    """
    transaction: Dict[str, Any] = {
        "id": 999999999,
        "state": "EXECUTED",
        "operationAmount": {"amount": "50.0", "currency": {"name": "EUR", "code": "EUR"}},
        "description": "Hotel booking",
    }

    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"RUB": 99.23}}
        mock_get.return_value = mock_response

        result = get_amount_in_rubles(transaction)

        # 50 EUR * 99.23 = 4961.5 RUB
        assert result == 4961.5
        assert isinstance(result, float)


def test_get_amount_in_rubles_missing_operation_amount() -> None:
    """
    Тест для транзакции без operationAmount.
    """
    transaction: Dict[str, Any] = {"id": 1, "description": "Missing operationAmount"}

    result = get_amount_in_rubles(transaction)

    assert result is None


def test_get_amount_in_rubles_missing_amount() -> None:
    """
    Тест для транзакции без поля amount в operationAmount.
    """
    transaction: Dict[str, Any] = {"operationAmount": {"currency": {"name": "руб.", "code": "RUB"}}}

    result = get_amount_in_rubles(transaction)

    assert result is None


def test_get_amount_in_rubles_missing_currency() -> None:
    """
    Тест для транзакции без поля currency в operationAmount.
    """
    transaction: Dict[str, Any] = {"operationAmount": {"amount": "100.0"}}

    result = get_amount_in_rubles(transaction)

    assert result is None


def test_get_amount_in_rubles_invalid_amount_type() -> None:
    """
    Тест для транзакции с некорректным типом суммы.
    """
    transaction: Dict[str, Any] = {
        "operationAmount": {"amount": "не число", "currency": {"name": "руб.", "code": "RUB"}}
    }

    result = get_amount_in_rubles(transaction)

    assert result is None


def test_get_amount_in_rubles_negative_amount() -> None:
    """
    Тест для транзакции с отрицательной суммой.
    """
    transaction: Dict[str, Any] = {
        "operationAmount": {"amount": "-100.0", "currency": {"name": "руб.", "code": "RUB"}}
    }

    result = get_amount_in_rubles(transaction)

    assert result is None


def test_get_amount_in_rubles_unsupported_currency() -> None:
    """
    Тест для транзакции с неподдерживаемой валютой.
    """
    transaction: Dict[str, Any] = {
        "operationAmount": {"amount": "100.0", "currency": {"name": "British Pound", "code": "GBP"}}
    }

    result = get_amount_in_rubles(transaction)

    assert result is None


def test_get_amount_in_rubles_empty_transaction() -> None:
    """
    Тест для пустой транзакции.
    """
    transaction: Dict[str, Any] = {}

    result = get_amount_in_rubles(transaction)

    assert result is None


def test_get_amount_in_rubles_invalid_currency_structure() -> None:
    """
    Тест для транзакции с некорректной структурой валюты.
    """
    transaction: Dict[str, Any] = {
        "operationAmount": {"amount": "100.0", "currency": "RUB"}  # Должен быть словарь, а не строка
    }

    result = get_amount_in_rubles(transaction)

    assert result is None


def test_convert_currency_apilayer_success() -> None:
    """
    Тест успешной конвертации валюты через API.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"RUB": 92.3}}
        mock_get.return_value = mock_response

        result = convert_currency_apilayer(100.0, "USD", "RUB")

        assert result == 9230.0
        assert isinstance(result, float)


def test_convert_currency_apilayer_api_failure() -> None:
    """
    Тест конвертации при ошибке API.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        result = convert_currency_apilayer(100.0, "USD", "RUB")

        assert result is None


def test_convert_currency_apilayer_no_api_key() -> None:
    """
    Тест конвертации без API ключа.
    """
    with patch("src.external_api.os.getenv") as mock_getenv:
        mock_getenv.return_value = None

        result = convert_currency_apilayer(100.0, "USD", "RUB")

        assert result is None


def test_convert_currency_apilayer_invalid_rate() -> None:
    """
    Тест конвертации с некорректным курсом.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"RUB": 0.0}}  # Некорректный курс
        mock_get.return_value = mock_response

        result = convert_currency_apilayer(100.0, "USD", "RUB")

        assert result is None


def test_convert_currency_apilayer_rate_not_found() -> None:
    """
    Тест конвертации когда курс не найден.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"EUR": 0.85}}  # Есть курс EUR, но нет RUB
        mock_get.return_value = mock_response

        result = convert_currency_apilayer(100.0, "USD", "RUB")

        assert result is None


def test_convert_currency_apilayer_api_success_false() -> None:
    """
    Тест конвертации когда API возвращает success: false.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
        mock_get.return_value = mock_response

        result = convert_currency_apilayer(100.0, "USD", "RUB")

        assert result is None


def test_convert_currency_apilayer_timeout() -> None:
    """
    Тест конвертации при таймауте запроса.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_get.side_effect = TimeoutError("Request timeout")

        result = convert_currency_apilayer(100.0, "USD", "RUB")

        assert result is None


def test_convert_currency_apilayer_connection_error() -> None:
    """
    Тест конвертации при ошибке подключения.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("Connection refused")

        result = convert_currency_apilayer(100.0, "USD", "RUB")

        assert result is None
