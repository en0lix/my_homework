"""
Модуль reports содержит функции для формирования отчётов.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


def spending_by_category(
    transactions: List[Dict[str, Any]],
    category: str,
    date: datetime | None = None,
) -> Dict[str, Any]:
    """
    Отчёт по тратам в указанной категории за последние 3 месяца.

    Args:
        transactions: Список транзакций.
        category: Категория.
        date: Конечная дата (по умолчанию — текущая).

    Returns:
        Словарь с отчётом.
    """
    if date is None:
        date = datetime.now()

    start_date = date.replace(day=1) - relativedelta(months=3)

    total = 0.0
    operations = []
    cat = category.lower()

    for tx in transactions:
        tx_date = tx.get("Дата операции")
        tx_category = str(tx.get("Категория", "")).lower()
        amount = tx.get("Сумма платежа", 0) or 0

        if (
            isinstance(tx_date, datetime)
            and start_date <= tx_date <= date
            and cat == tx_category
            and amount < 0
        ):
            total += abs(amount)
            operations.append(
                {
                    "date": tx_date.strftime("%d.%m.%Y"),
                    "amount": round(abs(amount), 2),
                    "description": tx.get("Описание", ""),
                }
            )

    return {
        "category": category,
        "period": f"{start_date.strftime('%d.%m.%Y')} — {date.strftime('%d.%m.%Y')}",
        "total_spent": round(total, 2),
        "operations": operations,
    }