import os
from typing import Any, Dict, Optional
from unittest.mock import patch

import requests
from dotenv import load_dotenv

load_dotenv()


def get_amount_in_rubles(transaction: Dict[str, Any]) -> Optional[float]:
    """
    Возвращает сумму транзакции в рублях для реальной структуры из operations.json.
    """
    try:
        # Проверяем, что транзакция не пустая
        if not transaction:
            print("❌ Пустая транзакция")
            return None

        # Извлекаем сумму и валюту из реальной структуры operations.json
        if 'operationAmount' not in transaction:
            print("❌ Отсутствует поле 'operationAmount' в транзакции")
            return None

        operation_amount = transaction['operationAmount']

        # Извлекаем сумму (она хранится как строка!)
        if 'amount' not in operation_amount:
            print("❌ Отсутствует поле 'amount' в operationAmount")
            return None

        amount_str = operation_amount['amount']

        # Конвертируем строку в число
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            print(f"❌ Некорректный формат суммы: '{amount_str}'")
            return None

        if amount < 0:
            print(f"❌ Отрицательная сумма: {amount}")
            return None

        # Извлекаем валюту из вложенной структуры
        if 'currency' not in operation_amount:
            print("❌ Отсутствует поле 'currency' в operationAmount")
            return None

        currency_data = operation_amount['currency']

        # Обрабатываем структуру валюты (словарь с полями 'name' и 'code')
        if not isinstance(currency_data, dict):
            print(f"❌ Некорректный формат валюты: {type(currency_data)}")
            return None

        if 'code' not in currency_data:
            print("❌ Отсутствует поле 'code' в currency")
            return None

        currency = currency_data['code'].upper()

        # Если валюта уже рубли, возвращаем как есть
        if currency == 'RUB':
            return amount

        # Если валюта USD или EUR, конвертируем
        if currency in ['USD', 'EUR']:
            converted_amount = convert_currency_apilayer(amount, currency, 'RUB')
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
    Конвертирует сумму из одной валюты в другую используя Exchange Rates Data API.
    """
    try:
        # Получаем API ключ из .env файла
        api_key = os.getenv('EXCHANGE_RATE_API_KEY')

        if not api_key:
            print("❌ API ключ не найден в .env файле")
            return None

        # Формируем URL для получения текущих курсов
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={from_currency}&symbols={to_currency}"

        headers = {'apikey': api_key}

        # Отправляем GET запрос
        response = requests.get(url, headers=headers, timeout=10)

        # Проверяем успешность запроса
        if response.status_code != 200:
            print(f"❌ HTTP ошибка {response.status_code}: {response.text[:100]}...")
            return None

        data = response.json()

        # Проверяем успешность ответа API
        if not data.get('success', False):
            error_info = data.get('error', {})
            print(f"❌ API ошибка: {error_info.get('info', 'Unknown error')}")
            return None

        # Получаем курс конвертации
        rates = data.get('rates', {})
        rate = rates.get(to_currency)

        if not rate:
            print(f"❌ Курс для {to_currency} не найден в ответе API")
            return None

        if rate <= 0:
            print(f"❌ Некорректный курс: {rate}")
            return None

        converted_amount = amount * rate
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


