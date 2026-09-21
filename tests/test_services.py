import pytest
from datetime import datetime

from src.services import filter_transactions_by_date, simple_search


@pytest.fixture
def transactions():
    return [
        {"Дата операции": datetime(2021, 12, 1), "Сумма платежа": -100, "Описание": "Колхоз", "Категория": "Супермаркеты"},
        {"Дата операции": datetime(2021, 12, 15), "Сумма платежа": -200, "Описание": "Магнит", "Категория": "Супермаркеты"},
        {"Дата операции": datetime(2021, 12, 31), "Сумма платежа": -300, "Описание": "Такси", "Категория": "Транспорт"},
        {"Дата операции": datetime(2021, 11, 30), "Сумма платежа": -400, "Описание": "Колхоз", "Категория": "Супермаркеты"},
    ]


def test_filter_transactions_by_date(transactions):
    result = filter_transactions_by_date(transactions, datetime(2021, 12, 20))
    assert len(result) == 2


def test_simple_search(transactions):
    result = simple_search(transactions, "колхоз")
    assert len(result) == 2


def test_simple_search_empty_query(transactions):
    assert simple_search(transactions, "") == []


def test_simple_search_no_match(transactions):
    assert simple_search(transactions, "ипотека") == []