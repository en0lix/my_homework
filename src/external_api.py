"""
Модуль external_api содержит функции для работы с внешними API.
"""

import os
from typing import Any, Dict, Optional

import requests

API_KEY = os.getenv('EXCHANGE_RATES_API_KEY', '')
BASE_URL = 'https://api.exchangeratesapi.io/v1/latest'


def convert_currency_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    """
    try:
        operation_amount = transaction.get("operationAmount", {})
        amount_str = operation_amount.get("amount", "0")
        currency_code = operation_amount.get("currency", {}).get("code", "RUB")

        amount = float(amount_str)

        if currency_code == "RUB":
            return amount

        rate = get_exchange_rate(currency_code, "RUB")

        if rate is None:
            return amount

        return amount * rate

    except (ValueError, TypeError, KeyError):
        return 0.0


def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]:
    """
    Получает курс валюты через внешнее API.
    """
    if not API_KEY:
        return None

    try:
        url = f"{BASE_URL}?access_key={API_KEY}&base={from_currency}&symbols={to_currency}"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get('success'):
            rates = data.get('rates', {})
            return rates.get(to_currency)

        return None

    except (requests.RequestException, ValueError, KeyError):
        return None