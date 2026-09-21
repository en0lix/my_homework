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

"""
Модуль external_api содержит функции для получения курсов валют и цен акций.
"""

import logging
import os
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY", "")
BASE_URL = "http://api.exchangeratesapi.io/v1/latest"


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """
    Получает курсы валют к рублю.

    Args:
        currencies: Список кодов валют.

    Returns:
        Список словарей с курсами.
    """
    if not API_KEY:
        logger.warning("API-ключ для валют не задан")
        return [{"currency": c, "rate": 0.0} for c in currencies]

    result = []
    for currency in currencies:
        try:
            url = f"{BASE_URL}?access_key={API_KEY}&base={currency}&symbols=RUB"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("success"):
                rate = data.get("rates", {}).get("RUB")
                result.append(
                    {"currency": currency, "rate": round(float(rate), 4) if rate else 0.0}
                )
            else:
                result.append({"currency": currency, "rate": 0.0})
        except Exception as e:
            logger.error(f"Ошибка получения курса {currency}: {e}")
            result.append({"currency": currency, "rate": 0.0})
    return result


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """
    Получает цены акций.

    Args:
        stocks: Список тикеров акций.

    Returns:
        Список словарей с ценами.
    """
    # Заглушка — реальный API зависит от выбранного провайдера
    return [{"stock": s, "price": 0.0} for s in stocks]


import os
import requests

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")


def get_stock_prices(stocks: List[str]) -> List[Dict[str, Any]]:
    """Получает цены акций через Finnhub."""
    if not FINNHUB_API_KEY:
        logger.warning("API-ключ для акций не задан")
        return [{"stock": s, "price": 0.0} for s in stocks]

    result = []
    for stock in stocks:
        try:
            url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={FINNHUB_API_KEY}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            price = data.get("c", 0.0)  # current price
            result.append({"stock": stock, "price": round(float(price), 2)})
        except Exception as e:
            logger.error(f"Ошибка получения цены {stock}: {e}")
            result.append({"stock": stock, "price": 0.0})
    return result

