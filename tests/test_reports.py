from datetime import datetime

from src.reports import spending_by_category


def test_spending_by_category():
    transactions = [
        {
            "Дата операции": datetime(2021, 12, 1),
            "Сумма платежа": -100,
            "Категория": "Супермаркеты",
            "Описание": "A",
        },
        {
            "Дата операции": datetime(2021, 12, 15),
            "Сумма платежа": -200,
            "Категория": "Супермаркеты",
            "Описание": "B",
        },
        {
            "Дата операции": datetime(2021, 12, 20),
            "Сумма платежа": -300,
            "Категория": "Транспорт",
            "Описание": "C",
        },
    ]
    result = spending_by_category(transactions, "Супермаркеты", datetime(2021, 12, 31))
    assert result["total_spent"] == 300
    assert len(result["operations"]) == 2
