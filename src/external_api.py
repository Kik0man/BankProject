import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


def get_amount_in_rubles(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Возвращает сумму транзакции в рублях.
    """
    try:
        # Извлекаем сумму и валюту из реальной структуры транзакции
        amount = transaction.get("amount")
        currency = transaction.get("currency", "RUB").upper()

        # Проверяем наличие и корректность суммы
        if amount is None:
            print("❌ Сумма транзакции отсутствует")
            return None

        if not isinstance(amount, (int, float)):
            print(f"❌ Некорректный тип суммы: {type(amount)}")
            return None

        if amount < 0:
            print(f"❌ Отрицательная сумма: {amount}")
            return None

        # Если валюта уже рубли, возвращаем как есть
        if currency == "RUB":
            return float(amount)

        # Если валюта USD или EUR, конвертируем
        if currency in ["USD", "EUR"]:
            converted_amount = convert_currency_apilayer(amount, currency, "RUB")
            if converted_amount is None:
                print(f"❌ Не удалось конвертировать {amount} {currency} в RUB")
                return None
            return converted_amount

        # Для других валют возвращаем ошибку
        print(f"❌ Неподдерживаемая валюта: {currency}")
        return None

    except Exception as e:
        print(f"❌ Неожиданная ошибка в get_amount_in_rubles: {e}")
        return None


def convert_currency_apilayer(amount: float, from_currency: str, to_currency: str) -> Optional[float]:
    """
    Конвертирует сумму из одной валюты в другую используя Exchange Rates Data API от apilayer.com.
    Args:
        amount: Сумма для конвертации
        from_currency: Исходная валюта (USD, EUR)
        to_currency: Целевая валюта (RUB)
    """
    try:
        # Получаем API ключ из .env файла
        api_key = os.getenv("EXCHANGE_RATE_API_KEY")

        if not api_key:
            print("❌ API ключ не найден в .env файле")
            return None

        # Формируем URL для получения текущих курсов
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={from_currency}&symbols={to_currency}"

        headers = {"apikey": api_key}

        # Отправляем GET запрос
        response = requests.get(url, headers=headers, timeout=10)

        # Проверяем успешность запроса
        if response.status_code != 200:
            print(f"❌ HTTP ошибка {response.status_code}: {response.text}")
            return None

        data = response.json()

        # Проверяем успешность ответа API
        if not data.get("success", False):
            error_info = data.get("error", {})
            print(f"❌ API ошибка: {error_info.get('info', 'Unknown error')}")
            return None

        # Получаем курс конвертации
        rates = data.get("rates", {})
        rate = rates.get(to_currency)

        if not rate:
            print(f"❌ Курс для {to_currency} не найден в ответе API")
            return None

        if rate <= 0:
            print(f"❌ Некорректный курс: {rate}")
            return None

        converted_amount = amount * rate

        print(f"✅ Конвертировано {amount} {from_currency} -> {converted_amount:.2f} {to_currency} (курс: {rate:.4f})")
        return float(converted_amount)

    except requests.exceptions.Timeout:
        print("❌ Таймаут подключения к API")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения к интернету")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
        return None
    except Exception as e:
        print(f"❌ Неожиданная ошибка в convert_currency_apilayer: {e}")
        return None
