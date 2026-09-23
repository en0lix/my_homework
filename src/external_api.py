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
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
BASE_URL = "http://api.exchangeratesapi.io/v1/latest"


def get_currency_rates(currencies: List[str]) -> List[Dict[str, Any]]:
    """
    Получает курсы валют к рублю.
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
    Получает цены акций через Finnhub.
    """
    if not FINNHUB_API_KEY:
        logger.warning("API-ключ для акций не задан")
        return [{"stock": s, "price": 0.0} for s in stocks]

    result = []
    for stock in stocks:
        try:
            url = f"https://finnhub.io/api/v1/quote" f"?symbol={stock}&token={FINNHUB_API_KEY}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            price = data.get("c", 0.0)
            result.append({"stock": stock, "price": round(float(price), 2)})
        except Exception as e:
            logger.error(f"Ошибка получения цены {stock}: {e}")
            result.append({"stock": stock, "price": 0.0})
    return result
