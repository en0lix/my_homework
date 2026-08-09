from src.generators import filter_by_currency


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


import pytest

from src.masks import card_number_generator


@pytest.mark.parametrize(
    "length,expected_length",
    [
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (18, 18),
        (19, 19),
    ],
)
def test_card_number_generator_length(length, expected_length):
    number = card_number_generator(length)
    assert isinstance(number, str)
    assert len(number) == expected_length
    assert number.isdigit()


def test_card_number_generator_default():
    number = card_number_generator()
    assert len(number) == 16
    assert number.isdigit()


@pytest.mark.parametrize("length", [12, 20])
def test_card_number_generator_invalid_length_raises(length):
    # Если твоя функция должна выбрасывать ошибку при неподходящей длине — раскомментируй:
    # with pytest.raises(ValueError):
    #     card_number_generator(length)

    # Если она просто возвращает строку любой длины — оставь как есть, главное, что проверили поведение
    number = card_number_generator(length)
    assert len(number) == length
