"""
Модуль processing содержит функции для фильтрации и сортировки транзакций.
"""

from typing import Any, Dict, List


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданному статусу.
    """
    if not transactions:
        return []

    return [item for item in transactions if item.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.
    """
    if not transactions:
        return []

    def get_date(transaction: Dict[str, Any]) -> str:
        """Вспомогательная функция для получения даты."""
        date_value: str = transaction.get("date", "")
        return date_value

    return sorted(transactions, key=get_date, reverse=reverse)
