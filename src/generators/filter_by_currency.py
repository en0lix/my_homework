def card_number_generator():
    """Заглушка для тестов — вернёт пример номера карты."""
    return "4111111111111111"

def filter_by_currency(transactions, currency):
    """
    Возвращает список транзакций, где валюта совпадает с указанной.

    :param transactions: список словарей, каждый с ключом 'currency'
    :param currency: строка с валютой, например 'RUB' или 'USD'
    :return: список подходящих транзакций
    """
    return [t for t in transactions if t.get("currency") == currency]


def filter_by_currency(transactions, currency):
    """
    Возвращает список транзакций, отфильтрованных по валюте.
    transactions: список словарей вида {"amount": 100, "currency": "USD", ...}
    currency: строка с валютой, например "USD"
    """
    return [t for t in transactions if t.get("currency") == currency]


from typing import Any, Dict, Iterable, Iterator, Optional


def filter_by_currency(transactions: Iterable[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """
    Возвращает итератор по транзакциям, где currency.code == currency.
    Пример: currency = "USD"
    """
    for t in transactions:
        amount = t.get("operationAmount", {})
        curr = amount.get("currency", {})
        code = curr.get("code")
        if code == currency:
            yield t


def transaction_descriptions(transactions: Iterable[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор описаний транзакций (поле description).
    Если описания нет — возвращает пустую строку.
    """
    for t in transactions:
        yield t.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генерирует номера карт в формате XXXX XXXX XXXX XXXX.
    start и end — целочисленные значения от 1 до 9999_9999_9999_9999.
    Выдаёт ровно end - start + 1 номеров (если start <= end).
    """
    if start > end or start < 1 or end > 9999_9999_9999_9999:
        return

    for number in range(start, end + 1):
        # Форматируем как 16 цифр с ведущими нулями, затем разбиваем на группы по 4
        s = f"{number:016d}"
        yield f"{s[0:4]} {s[4:8]} {s[8:12]} {s[12:16]}"
