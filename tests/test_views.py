from datetime import datetime

from src.views import get_cards_info, get_greeting, get_top_transactions


def test_get_greeting():
    result = get_greeting()
    assert result in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]


def test_get_cards_info():
    transactions = [
        {"Номер карты": "*7197", "Сумма платежа": -100, "Кэшбэк": 1},
        {"Номер карты": "*7197", "Сумма платежа": -200, "Кэшбэк": 2},
        {"Номер карты": "*5091", "Сумма платежа": -300, "Кэшбэк": 3},
    ]
    result = get_cards_info(transactions)
    assert len(result) == 2
    card = next(c for c in result if c["last_digits"] == "7197")
    assert card["total_spent"] == 300
    assert card["cashback"] == 3


def test_get_top_transactions():
    transactions = [
        {
            "Дата операции": datetime(2021, 12, 1),
            "Сумма платежа": -100,
            "Категория": "A",
            "Описание": "a",
        },
        {
            "Дата операции": datetime(2021, 12, 2),
            "Сумма платежа": -500,
            "Категория": "B",
            "Описание": "b",
        },
        {
            "Дата операции": datetime(2021, 12, 3),
            "Сумма платежа": -300,
            "Категория": "C",
            "Описание": "c",
        },
    ]
    result = get_top_transactions(transactions, limit=2)
    assert len(result) == 2
    assert result[0]["amount"] == -500
    assert result[1]["amount"] == -300
