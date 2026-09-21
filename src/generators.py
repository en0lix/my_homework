"""
Модуль generators содержит функции-генераторы для работы с транзакциями.
"""

from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте.
    """
    if not transactions:
        return

    for transaction in transactions:
        try:
            if (
                transaction.get("operationAmount")
                and transaction["operationAmount"].get("currency")
                and transaction["operationAmount"]["currency"].get("code") == currency
            ):
                yield transaction
        except (AttributeError, TypeError, KeyError):
            continue


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Возвращает итератор с описаниями транзакций.
    """
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int, end: int) -> Iterator[int]:
    """
    Генерирует номера карт в заданном диапазоне.
    """
    if start > end or start < 0:
        return

    for number in range(start, end + 1):
        card_number = int(f"100000000000000{number:01d}" if number < 10 else f"10000000000000{number:02d}")
        yield card_number
