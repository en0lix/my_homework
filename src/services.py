"""
Модуль services содержит бизнес-логику: фильтрация, поиск.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def _to_naive(dt: datetime | None) -> datetime | None:
    """Убирает временную зону у datetime, если она есть."""
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


def filter_transactions_by_date(
    transactions: List[Dict[str, Any]], end_date: datetime
) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции с начала месяца по указанную дату.
    """
    end_date = _to_naive(end_date)
    start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    result = []
    for tx in transactions:
        tx_date = _to_naive(tx.get("Дата операции"))
        if isinstance(tx_date, datetime) and start_date <= tx_date <= end_date:
            result.append(tx)
    return result


def simple_search(
    transactions: List[Dict[str, Any]], query: str
) -> List[Dict[str, Any]]:
    """
    Простой поиск по описанию и категории (регистронезависимый).
    """
    if not query:
        return []
    q = query.lower().strip()
    result = []
    for tx in transactions:
        description = str(tx.get("Описание", "")).lower()
        category = str(tx.get("Категория", "")).lower()
        if q in description or q in category:
            result.append(tx)
    return result