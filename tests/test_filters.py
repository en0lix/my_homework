import pytest

from src.generators import filter_by_currency



@pytest.mark.parametrize(
    "currency_code,expected_count",
    [
        ("USD", 2),
        ("RUB", 1),
        ("EUR", 0),
    ],
    ids=["usd_count", "rub_count", "eur_count"],
)
def test_filter_by_currency_counts(transactions, currency_code, expected_count):
    result = list(filter_by_currency(transactions, currency_code))
    assert len(result) == expected_count


def test_filter_by_currency_returns_iterator(transactions):
    iterator = filter_by_currency(transactions, "USD")
    # Проверяем, что это итератор и можно брать next
    first = next(iterator)
    assert first["currency"]["code"] == "USD"


def test_filter_by_currency_empty_list():
    transactions = []
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


def test_filter_by_currency_missing_fields():
    # Транзакция без operationAmount или без currency
    transactions = [
        {"id": 1},
        {"id": 2, "operationAmount": {}},
        {"id": 3, "operationAmount": {"currency": {}}},
        {"id": 4, "operationAmount": {"currency": {"code": "USD"}}},
    ]
    result = list(filter_by_currency(transactions, "USD"))
    # Должна пройти только транзакция с корректным кодом
    assert len(result) == 1
    assert result[0]["id"] == 4


# Фикстура для транзакций (можно вынести в conftest.py, если используешь глобально)
@pytest.fixture
def transactions():
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 123456789,
            "state": "EXECUTED",
            "date": "2018-07-01T10:00:00.000000",
            "operationAmount": {"amount": "1000.00", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Оплата услуг",
            "from": "Счет 00001111222233334444",
            "to": "Счет 55556666777788889999",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]
# tests/test_filters.py
from src.generators import filter_by_currency

def test_filter_by_currency_empty():
    assert filter_by_currency([], "RUB") == []

def test_filter_by_currency_mixed():
    transactions = [
        {"id": 1, "currency": "RUB"},
        {"id": 2, "currency": "USD"},
        {"id": 3, "currency": "RUB"},
    ]
    result = filter_by_currency(transactions, "RUB")
    assert len(result) == 2
    assert all(t["currency"] == "RUB" for t in result)
# src/generators.py

def filter_by_currency(transactions, currency):
    """
    Возвращает транзакции только указанной валюты.
    transactions: список словарей, каждый с ключом 'currency'
    currency: строка, например 'RUB'
    """
    return [t for t in transactions if t.get("currency") == currency]
