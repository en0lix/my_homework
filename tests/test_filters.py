import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


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
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 123456789,
            "state": "EXECUTED",
            "date": "2020-01-01T12:00:00.000000",
            "operationAmount": {"amount": "1000.00", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Оплата услуг",
            "from": "Карта 1234 5678 9012 3456",
            "to": "Сервис XYZ",
        },
    ]


class TestFilterByCurrency:
    @pytest.mark.parametrize(
        "currency,expected_count",
        [
            ("USD", 2),
            ("RUB", 1),
            ("EUR", 0),
        ],
    )
    def test_filter_by_currency_count(self, transactions, currency, expected_count):
        result = list(filter_by_currency(transactions, currency))
        assert len(result) == expected_count

    def test_filter_by_currency_empty_list(self):
        assert list(filter_by_currency([], "USD")) == []

    def test_filter_by_currency_no_matching_currency(self):
        txs = [
            {"operationAmount": {"currency": {"code": "EUR"}}},
            {"operationAmount": {"currency": {"code": "JPY"}}},
        ]
        assert list(filter_by_currency(txs, "USD")) == []

    def test_filter_by_currency_missing_fields(self):
        txs = [
            {},  # нет operationAmount
            {"operationAmount": {}},  # нет currency
            {"operationAmount": {"currency": {}}},  # нет code
        ]
        assert list(filter_by_currency(txs, "USD")) == []


class TestTransactionDescriptions:
    def test_descriptions_all_present(self, transactions):
        descs = list(transaction_descriptions(transactions))
        expected = ["Перевод организации", "Перевод со счета на счет", "Оплата услуг"]
        assert descs == expected

    @pytest.mark.parametrize(
        "txs,expected",
        [
            ([], []),
            ([{"description": "A"}], ["A"]),
            ([{}, {"description": ""}], ["", ""]),
        ],
    )
    def test_descriptions_edge_cases(self, txs, expected):
        assert list(transaction_descriptions(txs)) == expected


class TestCardNumberGenerator:
    @pytest.mark.parametrize(
        "start,end,expected",
        [
            (1, 1, ["0000 0000 0000 0001"]),
            (5, 5, ["0000 0000 0000 0005"]),
            (
                9999999999999995,
                9999999999999999,
                [
                    "9999 9999 9999 9995",
                    "9999 9999 9999 9996",
                    "9999 9999 9999 9997",
                    "9999 9999 9999 9998",
                    "9999 9999 9999 9999",
                ],
            ),
        ],
    )
    def test_card_number_generator_basic(self, start, end, expected):
        assert list(card_number_generator(start, end)) == expected

    def test_card_number_generator_invalid_range(self):
        assert list(card_number_generator(10, 5)) == []
        assert list(card_number_generator(-1, 5)) == []
        assert list(card_number_generator(1, 10**17)) == []

    def test_card_number_format(self):
        gen = card_number_generator(123, 123)
        res = next(gen)
        parts = res.split(" ")
        assert len(parts) == 4
        assert all(len(p) == 4 and p.isdigit() for p in parts)
