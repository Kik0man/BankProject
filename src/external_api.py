import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


def get_amount_in_rubles(transaction: Dict[str, Any]) -> float:
    """
    Возвращает сумму транзакции в рублях.
    """
    # Получаем сумму и валюту из транзакции
    amount = transaction.get("amount", 0.0)
    currency = transaction.get("currency", "RUB").upper()

    # Если сумма не число, возвращаем 0
    if not isinstance(amount, (int, float)):
        return 0.0

    # Если валюта уже рубли, возвращаем как есть
    if currency == "RUB":
        return float(amount)

    # Если валюта USD или EUR, конвертируем
    if currency in ["USD", "EUR"]:
        return convert_currency_apilayer(amount, currency, "RUB")  # ← ИСПРАВЛЕНО ИМЯ ФУНКЦИИ

    # Для других валют возвращаем исходную сумму
    return float(amount)


def convert_currency_apilayer(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Конвертирует сумму из одной валюты в другую используя Exchange Rates Data API от apilayer.com.
    """
    try:
        # Получаем API ключ из .env файла
        api_key = os.getenv("EXCHANGE_RATE_API_KEY")

        if not api_key:
            print("❌ API ключ не найден в .env файле")
            print("   Добавьте EXCHANGE_RATE_API_KEY=ваш_ключ в файл .env")
            return float(amount)

        # ВАРИАНТ 1: Используем endpoint для текущих курсов (без даты)
        url = f"https://api.apilayer.com/exchangerates_data/latest?base={from_currency}&symbols={to_currency}"

        # ВАРИАНТ 2: Или используем convert endpoint
        # url = f"https://api.apilayer.com/exchangerates_data/convert?
        # to={to_currency}&from={from_currency}&amount={amount}"

        # Заголовки как в примере curl
        headers = {"apikey": api_key}

        # Отправляем GET запрос
        response = requests.get(url, headers=headers, timeout=10)

        # Проверяем успешность запроса
        if response.status_code == 200:
            data = response.json()

            # Проверяем успешность ответа API
            if data.get("success", False):
                # Получаем курс конвертации
                rates = data.get("rates", {})
                rate = rates.get(to_currency)

                if rate:
                    converted_amount = amount * rate
                    print(
                        f"✅ Конвертировано {amount} {from_currency} -> {converted_amount:.2f} "
                        f"{to_currency} (курс: {rate:.4f})"
                    )
                    return float(converted_amount)
                else:
                    print(f"❌ Курс для {to_currency} не найден в ответе API")
                    return float(amount)
            else:
                error_info = data.get("error", {})
                print(f"❌ Ошибка API: {error_info.get('info', 'Unknown error')}")
                return float(amount)

        else:
            print(f"❌ HTTP ошибка: {response.status_code} - {response.text}")
            return float(amount)

    except requests.exceptions.Timeout:
        print("❌ Таймаут подключения к API")
        return float(amount)
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения к интернету")
        return float(amount)
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
        return float(amount)
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return float(amount)
