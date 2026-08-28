from typing import Any, Dict, List, Optional


def filter_by_state(transactions: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданному статусу.

    Args:
        transactions: Список словарей с данными транзакций
        state: Статус для фильтрации (по умолчанию "EXECUTED")

    Returns:
        List[Dict[str, Any]]: Отфильтрованный список транзакций
    """
    if not transactions:
        return []

    return [item for item in transactions if item.get("state") == state]


def sort_by_date(transactions: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует транзакции по дате.

    Args:
        transactions: Список словарей с данными транзакций
        reverse: True - по убыванию (новые сверху), False - по возрастанию

    Returns:
        List[Dict[str, Any]]: Отсортированный список транзакций
    """
    if not transactions:
        return []

    def get_date(transaction: Dict[str, Any]) -> str:
        """
        Вспомогательная функция для получения даты из транзакции.
        Если ключ 'date' отсутствует, возвращает пустую строку.
        """
        return transaction.get("date", "")

    return sorted(transactions, key=get_date, reverse=reverse)
