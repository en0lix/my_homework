from generators import filter_by_currency


def test_filter_by_currency_usd():
    transactions = [
        {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
        {"id": 2, "operationAmount": {"currency": {"code": "RUB"}}},
        {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
    ]
    usd_iter = filter_by_currency(transactions, "USD")
    assert next(usd_iter)["id"] == 1
    assert next(usd_iter)["id"] == 3


def test_filter_by_currency_empty():
    transactions = [{"id": 1, "operationAmount": {"currency": {"code": "RUB"}}}]
    usd_iter = filter_by_currency(transactions, "USD")
    try:
        next(usd_iter)
        assert False, "Должен быть StopIteration"
    except StopIteration:
        pass
