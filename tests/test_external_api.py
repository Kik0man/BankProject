from typing import Any, Dict
from unittest.mock import Mock, patch

from src.external_api import convert_currency_apilayer, get_amount_in_rubles


def test_get_amount_in_rubles_rub_currency() -> None:
    """
    Тест для транзакции в рублях (без конвертации).
    """
    transaction: Dict[str, Any] = {"id": 1, "amount": 100.50, "currency": "RUB", "description": "Test transaction"}

    result: float = get_amount_in_rubles(transaction)

    assert result == 100.50
    assert isinstance(result, float)


def test_get_amount_in_rubles_usd_currency() -> None:
    """
    Тест для транзакции в USD с моком API.
    """
    transaction: Dict[str, Any] = {"id": 2, "amount": 100.0, "currency": "USD", "description": "Test USD transaction"}

    # Мокаем API запрос - исправлен путь!
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"RUB": 90.5}}
        mock_get.return_value = mock_response

        result: float = get_amount_in_rubles(transaction)

        # 100 USD * 90.5 = 9050 RUB
        assert result == 9050.0
        assert isinstance(result, float)


def test_get_amount_in_rubles_eur_currency() -> None:
    """
    Тест для транзакции в EUR с моком API.
    """
    transaction: Dict[str, Any] = {"id": 3, "amount": 50.0, "currency": "EUR", "description": "Test EUR transaction"}

    # Исправлен путь для мока!
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"RUB": 95.2}}
        mock_get.return_value = mock_response

        result: float = get_amount_in_rubles(transaction)

        # 50 EUR * 95.2 = 4760 RUB
        assert result == 4760.0
        assert isinstance(result, float)


def test_get_amount_in_rubles_invalid_amount() -> None:
    """
    Тест для транзакции с невалидной суммой.
    """
    transaction: Dict[str, Any] = {
        "id": 4,
        "amount": "invalid",  # Строка вместо числа
        "currency": "RUB",
        "description": "Invalid amount transaction",
    }

    result: float = get_amount_in_rubles(transaction)

    assert result == 0.0
    assert isinstance(result, float)


def test_get_amount_in_rubles_missing_amount() -> None:
    """
    Тест для транзакции без суммы.
    """
    transaction: Dict[str, Any] = {"id": 5, "currency": "RUB", "description": "Missing amount transaction"}

    result: float = get_amount_in_rubles(transaction)

    assert result == 0.0
    assert isinstance(result, float)


def test_get_amount_in_rubles_missing_currency() -> None:
    """
    Тест для транзакции без валюты (должна использоваться RUB по умолчанию).
    """
    transaction: Dict[str, Any] = {"id": 6, "amount": 200.0, "description": "Missing currency transaction"}

    result: float = get_amount_in_rubles(transaction)

    assert result == 200.0
    assert isinstance(result, float)


def test_get_amount_in_rubles_unknown_currency() -> None:
    """
    Тест для транзакции с неизвестной валютой.
    """
    transaction: Dict[str, Any] = {
        "id": 7,
        "amount": 150.0,
        "currency": "GBP",  # Не поддерживаемая валюта
        "description": "Unknown currency transaction",
    }

    result: float = get_amount_in_rubles(transaction)

    assert result == 150.0
    assert isinstance(result, float)


def test_convert_currency_apilayer_success() -> None:
    """
    Тест успешной конвертации валюты через API.
    """
    # Исправлен путь для мока!
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"RUB": 92.3}}
        mock_get.return_value = mock_response

        result: float = convert_currency_apilayer(100.0, "USD", "RUB")

        # 100 USD * 92.3 = 9230 RUB
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

        result: float = convert_currency_apilayer(100.0, "USD", "RUB")

        # При ошибке API должна вернуться исходная сумма
        assert result == 100.0
        assert isinstance(result, float)


def test_convert_currency_apilayer_network_error() -> None:
    """
    Тест конвертации при сетевой ошибке.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")

        result: float = convert_currency_apilayer(100.0, "USD", "RUB")

        # При сетевой ошибке должна вернуться исходная сумма
        assert result == 100.0
        assert isinstance(result, float)


def test_convert_currency_apilayer_no_api_key() -> None:
    """
    Тест конвертации без API ключа.
    """
    # Исправлен путь для мока!
    with patch("src.external_api.os.getenv") as mock_getenv:
        mock_getenv.return_value = None  # Нет API ключа

        result: float = convert_currency_apilayer(100.0, "USD", "RUB")

        # Без API ключа должна вернуться исходная сумма
        assert result == 100.0
        assert isinstance(result, float)


def test_convert_currency_apilayer_invalid_json_response() -> None:
    """
    Тест конвертации при некорректном JSON ответе от API.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response

        result: float = convert_currency_apilayer(100.0, "USD", "RUB")

        # При ошибке парсинга JSON должна вернуться исходная сумма
        assert result == 100.0
        assert isinstance(result, float)


def test_convert_currency_apilayer_rate_not_found() -> None:
    """
    Тест конвертации когда курс не найден в ответе API.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"EUR": 0.85}}  # Есть курс EUR, но нет RUB
        mock_get.return_value = mock_response

        result: float = convert_currency_apilayer(100.0, "USD", "RUB")

        # Если курс не найден, должна вернуться исходная сумма
        assert result == 100.0
        assert isinstance(result, float)


def test_convert_currency_apilayer_api_success_false() -> None:
    """
    Тест конвертации когда API возвращает success: false.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
        mock_get.return_value = mock_response

        result: float = convert_currency_apilayer(100.0, "USD", "RUB")

        # При success: false должна вернуться исходная сумма
        assert result == 100.0
        assert isinstance(result, float)


def test_convert_currency_apilayer_timeout() -> None:
    """
    Тест конвертации при таймауте запроса.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_get.side_effect = TimeoutError("Request timeout")

        result: float = convert_currency_apilayer(100.0, "USD", "RUB")

        # При таймауте должна вернуться исходная сумма
        assert result == 100.0
        assert isinstance(result, float)


def test_convert_currency_apilayer_connection_error() -> None:
    """
    Тест конвертации при ошибке подключения.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_get.side_effect = ConnectionError("Connection refused")

        result: float = convert_currency_apilayer(100.0, "USD", "RUB")

        # При ошибке подключения должна вернуться исходная сумма
        assert result == 100.0
        assert isinstance(result, float)
