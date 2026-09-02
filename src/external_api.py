"""
Модуль external_api содержит функции для работы с внешними API.
"""

import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# API ключ из переменных окружения
API_KEY = os.getenv('EXCHANGE_RATES_API_KEY', '')
BASE_URL = 'http://api.exchangeratesapi.io/v1/latest'  # Используем HTTP, не HTTPS


def convert_currency_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        float: Сумма транзакции в рублях

    Пример:
        >>> transaction = {
        ...     "operationAmount": {
        ...         "amount": "100",
        ...         "currency": {"code": "USD"}
        ...     }
        ... }
        >>> convert_currency_to_rub(transaction)
        8500.0
    """
    try:
        # Получаем сумму и валюту из транзакции
        operation_amount = transaction.get("operationAmount", {})
        amount_str = operation_amount.get("amount", "0")
        currency_code = operation_amount.get("currency", {}).get("code", "RUB")

        # Преобразуем сумму в float
        amount = float(amount_str)

        # Если валюта уже рубли, возвращаем сумму
        if currency_code == "RUB":
            return amount

        # Получаем курс валюты к рублю
        rate = get_exchange_rate(currency_code, "RUB")

        # Если не удалось получить курс, возвращаем исходную сумму
        if rate is None:
            return amount

        # Конвертируем сумму в рубли
        return amount * rate

    except (ValueError, TypeError, KeyError) as e:
        # Логируем ошибку
        print(f"Error converting currency: {e}")
        return 0.0


def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]:
    """
    Получает курс валюты через внешнее API.

    Args:
        from_currency: Код исходной валюты (например, "USD")
        to_currency: Код целевой валюты (например, "RUB")

    Returns:
        Optional[float]: Курс валюты или None в случае ошибки

    Пример:
        >>> get_exchange_rate("USD", "RUB")
        85.5
    """
    # Проверяем наличие API ключа
    if not API_KEY:
        print("Warning: EXCHANGE_RATES_API_KEY not set")
        return None

    try:
        # Формируем URL для запроса
        # Используем параметры: access_key, base, symbols
        url = f"{BASE_URL}?access_key={API_KEY}&base={from_currency}&symbols={to_currency}"

        # Отправляем запрос
        response = requests.get(url, timeout=10)

        # Проверяем статус ответа
        response.raise_for_status()

        # Парсим JSON ответ
        data = response.json()

        # Проверяем успешность запроса
        if data.get('success'):
            rates = data.get('rates', {})
            rate = rates.get(to_currency)

            if rate is not None:
                return float(rate)

        # Если не удалось получить курс, логируем ошибку
        print(f"Error getting exchange rate: {data}")
        return None

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except (ValueError, KeyError) as e:
        print(f"Parse error: {e}")
        return None