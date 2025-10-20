from typing import Any, Dict, Optional
from unittest.mock import Mock, patch


from src.external_api import convert_currency_apilayer, get_amount_in_rubles


def test_get_amount_in_rubles_real_transaction_structure() -> None:
    """
    Тест для реальной структуры транзакции.
    """
    test_transaction = {"amount": 31957.58, "currency": "RUB", "description": "Перевод организации"}

    result: Optional[float] = get_amount_in_rubles(test_transaction)

    assert result == 31957.58
    assert isinstance(result, float)


def test_get_amount_in_rubles_usd_transaction() -> None:
    """
    Тест для транзакции в USD.
    """
    transaction: Dict[str, Any] = {"amount": 100.0, "currency": "USD", "description": "Payment for services"}

    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"RUB": 91.45}}
        mock_get.return_value = mock_response

        result: Optional[float] = get_amount_in_rubles(transaction)

        # 100 USD * 91.45 = 9145 RUB
        assert result == 9145.0
        assert isinstance(result, float)


def test_get_amount_in_rubles_eur_transaction() -> None:
    """
    Тест для транзакции в EUR.
    """
    transaction: Dict[str, Any] = {"amount": 50.0, "currency": "EUR", "description": "Hotel booking"}

    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"RUB": 99.23}}
        mock_get.return_value = mock_response

        result: Optional[float] = get_amount_in_rubles(transaction)

        # 50 EUR * 99.23 = 4961.5 RUB
        assert result == 4961.5
        assert isinstance(result, float)


def test_get_amount_in_rubles_missing_amount() -> None:
    """
    Тест для транзакции без суммы.
    """
    transaction: Dict[str, Any] = {"currency": "RUB", "description": "Missing amount transaction"}

    result: Optional[float] = get_amount_in_rubles(transaction)

    assert result is None


def test_get_amount_in_rubles_invalid_amount_type() -> None:
    """
    Тест для транзакции с некорректным типом суммы.
    """
    transaction: Dict[str, Any] = {"amount": "invalid_string", "currency": "RUB", "description": "Invalid amount type"}

    result: Optional[float] = get_amount_in_rubles(transaction)

    assert result is None


def test_get_amount_in_rubles_negative_amount() -> None:
    """
    Тест для транзакции с отрицательной суммой.
    """
    transaction: Dict[str, Any] = {"amount": -100.0, "currency": "RUB", "description": "Negative amount"}

    result: Optional[float] = get_amount_in_rubles(transaction)

    assert result is None


def test_get_amount_in_rubles_unsupported_currency() -> None:
    """
    Тест для транзакции с неподдерживаемой валютой.
    """
    transaction: Dict[str, Any] = {"amount": 100.0, "currency": "GBP", "description": "British pounds"}

    result: Optional[float] = get_amount_in_rubles(transaction)

    assert result is None


def test_convert_currency_apilayer_success() -> None:
    """
    Тест успешной конвертации.
    """
    with patch("src.external_api.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True, "rates": {"RUB": 92.3}}
        mock_get.return_value = mock_response

        result: Optional[float] = convert_currency_apilayer(100.0, "USD", "RUB")

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

        result: Optional[float] = convert_currency_apilayer(100.0, "USD", "RUB")

        assert result is None


def test_convert_currency_apilayer_no_api_key() -> None:
    """
    Тест конвертации без API ключа.
    """
    with patch("src.external_api.os.getenv") as mock_getenv:
        mock_getenv.return_value = None

        result: Optional[float] = convert_currency_apilayer(100.0, "USD", "RUB")

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

        result: Optional[float] = convert_currency_apilayer(100.0, "USD", "RUB")

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

        result: Optional[float] = convert_currency_apilayer(100.0, "USD", "RUB")

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

        result: Optional[float] = convert_currency_apilayer(100.0, "USD", "RUB")

        assert result is None


def test_comprehensive_transaction_test() -> None:
    """
    Комплексный тест с различными типами транзакций.
    """
    test_cases = [
        # (transaction, expected_result, description)
        ({"amount": 100.0, "currency": "RUB"}, 100.0, "Рубли без конвертации"),
        ({"amount": 0.0, "currency": "RUB"}, 0.0, "Нулевая сумма"),
        ({"amount": 1000.0, "currency": "USD"}, 91500.0, "Доллары с конвертацией"),  # 1000 * 91.5
        ({"amount": 500.0, "currency": "EUR"}, 49615.0, "Евро с конвертацией"),  # 500 * 99.23
    ]

    for transaction, expected, description in test_cases:
        with patch("src.external_api.requests.get") as mock_get:
            # Настраиваем мок для USD/EUR транзакций
            if transaction.get("currency") in ["USD", "EUR"]:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "success": True,
                    "rates": {"RUB": 91.5 if transaction["currency"] == "USD" else 99.23},
                }
                mock_get.return_value = mock_response

            result = get_amount_in_rubles(transaction)
            assert result == expected, f"Тест не пройден: {description}"
            print(f"✅ {description}: {transaction['amount']} {transaction['currency']} -> {result} RUB")
