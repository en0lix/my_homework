# src/generators.py

from typing import Any, Dict, Iterator, Optional


def filter_by_currency(transactions: list[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.

    Args:
        transactions: Список словарей с данными транзакций
        currency: Код валюты для фильтрации (например, "USD")

    Yields:
        Iterator[Dict[str, Any]]: Итератор с транзакциями в указанной валюте

    Example:
        >>> transactions = [
        ...     {"id": 1, "operationAmount": {"currency": {"code": "USD"}, "amount": "100"}},
        ...     {"id": 2, "operationAmount": {"currency": {"code": "EUR"}, "amount": "200"}},
        ...     {"id": 3, "operationAmount": {"currency": {"code": "USD"}, "amount": "300"}},
        ... ]
        >>> for transaction in filter_by_currency(transactions, "USD"):
        ...     print(transaction["id"])
        1
        3
    """
    if not transactions:
        return

    for transaction in transactions:
        try:
            # Проверяем наличие валюты в транзакции
            if (
                transaction.get("operationAmount")
                and transaction["operationAmount"].get("currency")
                and transaction["operationAmount"]["currency"].get("code") == currency
            ):
                yield transaction
        except (AttributeError, TypeError, KeyError):
            # Пропускаем транзакции с некорректной структурой
            continue


def transaction_descriptions(transactions: list[Dict[str, Any]]) -> Iterator[str]:
    """
    Возвращает итератор с описаниями транзакций.

    Args:
        transactions: Список словарей с данными транзакций

    Yields:
        Iterator[str]: Итератор с описаниями транзакций

    Example:
        >>> transactions = [
        ...     {"description": "Payment for services"},
        ...     {"description": "Online purchase"},
        ... ]
        >>> list(transaction_descriptions(transactions))
        ['Payment for services', 'Online purchase']
    """
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int, end: int) -> Iterator[int]:
    """
    Генерирует номера карт в заданном диапазоне.

    Args:
        start: Начальное значение (включительно)
        end: Конечное значение (включительно)

    Yields:
        Iterator[int]: Итератор с номерами карт (16-значные числа)

    Example:
        >>> list(card_number_generator(1, 3))
        [1000000000000001, 1000000000000002, 1000000000000003]
    """
    if start > end or start < 0:
        return

    for number in range(start, end + 1):
        # Форматируем номер карты как 16-значное число
        card_number = int(f"100000000000000{number:01d}" if number < 10 else f"10000000000000{number:02d}")
        yield card_number
