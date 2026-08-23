from typing import List, Dict, Any, Optional


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданному статусу.

    Args:
        transactions: Список словарей с данными транзакций
        state: Статус для фильтрации (по умолчанию "EXECUTED")

    Returns:
        List[Dict[str, Any]]: Отфильтрованный список транзакций

    Example:
        >>> transactions = [
        ...     {"id": 1, "state": "EXECUTED"},
        ...     {"id": 2, "state": "PENDING"},
        ...     {"id": 3, "state": "EXECUTED"},
        ... ]
        >>> filter_by_state(transactions, "EXECUTED")
        [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]
    """
    if not transactions:
        return []

    return [item for item in transactions if item.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Args:
        transactions: Список словарей с данными транзакций
        reverse: True - по убыванию (новые сверху), False - по возрастанию (старые сверху)

    Returns:
        List[Dict[str, Any]]: Отсортированный список транзакций

    Example:
        >>> transactions = [
        ...     {"id": 1, "date": "2026-08-22T10:00:00"},
        ...     {"id": 2, "date": "2026-08-21T15:30:00"},
        ...     {"id": 3, "date": "2026-08-20T09:15:00"},
        ... ]
        >>> sort_by_date(transactions, reverse=True)  # По убыванию (новые → старые)
        [{"id": 1, ...}, {"id": 2, ...}, {"id": 3, ...}]
        >>> sort_by_date(transactions, reverse=False)  # По возрастанию (старые → новые)
        [{"id": 3, ...}, {"id": 2, ...}, {"id": 1, ...}]
    """
    if not transactions:
        return []

    def get_date(transaction: Dict[str, Any]) -> str:
        """
        Вспомогательная функция для получения даты из транзакции.
        Если ключ 'date' отсутствует, возвращает пустую строку.
        """
        return transaction.get("date", "")

    # Сортируем с использованием ключа и параметра reverse
    return sorted(transactions, key=get_date, reverse=reverse)