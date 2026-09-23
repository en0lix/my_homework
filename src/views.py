"""
Модуль views содержит функции для генерации JSON-ответов веб-страниц.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from src.services import filter_transactions_by_date

logger = logging.getLogger(__name__)


def get_greeting() -> str:
    """
    Возвращает приветствие в зависимости от текущего времени.

    Returns:
        Строка приветствия.
    """
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_cards_info(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Формирует информацию по каждой карте/счету.
    Поддерживает два формата: "Номер карты" и "Откуда".

    Args:
        transactions: Список транзакций.

    Returns:
        Список словарей по каждой карте.
    """
    cards: Dict[str, Dict[str, Any]] = {}

    for tx in transactions:
        card = str(tx.get("Номер карты", "")).strip()

        # Если нет "Номер карты", берём из "Откуда"
        if not card:
            from_field = str(tx.get("Откуда", "") or tx.get("from", ""))
            digits = "".join(c for c in from_field if c.isdigit())
            if len(digits) >= 4:
                card = digits

        if not card:
            continue

        amount = tx.get("Сумма платежа", 0) or 0
        cashback = tx.get("Кэшбэк", 0) or 0

        if card not in cards:
            cards[card] = {
                "last_digits": card[-4:],
                "total_spent": 0.0,
                "cashback": 0.0,
            }

        if amount < 0:
            cards[card]["total_spent"] += abs(amount)
        cards[card]["cashback"] += cashback

    result = []
    for card_data in cards.values():
        result.append(
            {
                "last_digits": card_data["last_digits"],
                "total_spent": round(card_data["total_spent"], 2),
                "cashback": round(card_data["cashback"], 2),
            }
        )
    return result


def get_top_transactions(
    transactions: List[Dict[str, Any]], limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Возвращает топ-N транзакций по сумме платежа (по модулю), по убыванию.

    Args:
        transactions: Список транзакций.
        limit: Количество транзакций.

    Returns:
        Список топ-N транзакций.
    """
    sorted_tx = sorted(
        transactions,
        key=lambda x: abs(x.get("Сумма платежа", 0) or 0),
        reverse=True,
    )[:limit]

    return [
        {
            "date": (tx.get("Дата операции") or datetime.now()).strftime("%d.%m.%Y"),
            "amount": round(tx.get("Сумма платежа", 0) or 0, 2),
            "category": tx.get("Категория", ""),
            "description": tx.get("Описание", ""),
        }
        for tx in sorted_tx
    ]


def get_main_page_view(
    date_str: str,
    transactions: List[Dict[str, Any]],
    currency_rates: List[Dict[str, Any]],
    stock_prices: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Формирует JSON-ответ для главной страницы.

    Args:
        date_str: Дата в формате YYYY-MM-DD HH:MM:SS.
        transactions: Список транзакций.
        currency_rates: Курсы валют.
        stock_prices: Цены акций.

    Returns:
        JSON-ответ.
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    filtered = filter_transactions_by_date(transactions, dt)

    return {
        "greeting": get_greeting(),
        "cards": get_cards_info(filtered),
        "top_transactions": get_top_transactions(filtered),
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
