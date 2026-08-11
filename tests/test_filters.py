import pytest

from generators import filter_by_currency


@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "amount": 100, "currency": "USD"},
        {"id": 2, "amount": 200, "currency": "rub"},
        {"id": 3, "amount": 300, "currency": "EUR"},
        {"id": 4, "amount": 400, "currency": "usd"},
        {"id": 5, "amount": 500},  # нет валюты
    ]


def test_filter_by_currency_usd(sample_transactions):
    result = filter_by_currency(sample_transactions, "USD")
    assert len(result) == 2
    ids = {t["id"] for t in result}
    assert ids == {1, 4}


def test_filter_by_currency_rub_case_insensitive(sample_transactions):
    result = filter_by_currency(sample_transactions, "rub")
    assert len(result) == 1
    assert result[0]["id"] == 2


@pytest.mark.parametrize(
    "currency, expected_ids",
    [
        ("EUR", {3}),
        ("eur", {3}),
        ("USD", {1, 4}),
        ("RUB", {2}),
    ],
)
def test_filter_by_currency_parametrized(sample_transactions, currency, expected_ids):
    result = filter_by_currency(sample_transactions, currency)
    ids = {t["id"] for t in result}
    assert ids == expected_ids


def test_filter_by_currency_empty_list():
    assert filter_by_currency([], "USD") == []


def test_filter_by_currency_invalid_type_transactions():
    with pytest.raises(TypeError):
        filter_by_currency("not a list", "USD")  # type: ignore


def test_filter_by_currency_invalid_type_currency():
    with pytest.raises(TypeError):
        filter_by_currency([{"id": 1, "currency": "USD"}], 123)  # type: ignore
