import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# ==================== ФИКСТУРЫ ====================


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями разных валют"""
    return [
        {
            "id": 1,
            "operationAmount": {"currency": {"code": "USD"}, "amount": "100.50"},
            "description": "Payment for services",
        },
        {
            "id": 2,
            "operationAmount": {"currency": {"code": "EUR"}, "amount": "250.00"},
            "description": "Online purchase",
        },
        {
            "id": 3,
            "operationAmount": {"currency": {"code": "USD"}, "amount": "75.20"},
            "description": "Transfer to friend",
        },
        {"id": 4, "operationAmount": {"currency": {"code": "RUB"}, "amount": "5000.00"}, "description": "Groceries"},
        {
            "id": 5,
            "operationAmount": {"currency": {"code": "USD"}, "amount": "1200.00"},
            "description": "Rent payment",
        },
        {"id": 6, "operationAmount": {"currency": {"code": "GBP"}, "amount": "300.00"}, "description": "Subscription"},
    ]


@pytest.fixture
def empty_transactions():
    """Фикстура с пустым списком транзакций"""
    return []


# ==================== ТЕСТЫ ДЛЯ filter_by_currency ====================


class TestFilterByCurrency:
    """Класс тестов для функции filter_by_currency"""

    @pytest.mark.parametrize(
        "currency, expected_ids",
        [
            ("USD", [1, 3, 5]),
            ("EUR", [2]),
            ("RUB", [4]),
            ("GBP", [6]),
        ],
    )
    def test_filter_by_currency_valid(self, sample_transactions, currency, expected_ids):
        """Тест фильтрации по валюте"""
        result = list(filter_by_currency(sample_transactions, currency))
        assert len(result) == len(expected_ids)
        assert [item["id"] for item in result] == expected_ids
        for item in result:
            assert item["operationAmount"]["currency"]["code"] == currency

    @pytest.mark.parametrize("currency", ["JPY", "CHF", "CAD", "AUD", "CNY"])
    def test_filter_by_currency_not_found(self, sample_transactions, currency):
        """Тест, когда транзакции в заданной валюте отсутствуют"""
        result = list(filter_by_currency(sample_transactions, currency))
        assert result == []

    def test_filter_by_currency_empty_list(self, empty_transactions):
        """Тест с пустым списком транзакций (строка 9)"""
        result = list(filter_by_currency(empty_transactions, "USD"))
        assert result == []

    def test_filter_by_currency_missing_currency_key(self):
        """Тест с транзакциями без ключа currency (строка 18)"""
        transactions = [
            {"operationAmount": {"currency": {"code": "USD"}}},
            {"operationAmount": {}},
            {"operationAmount": {"currency": {"code": "EUR"}}},
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 1

    def test_filter_by_currency_mixed_data(self):
        """Тест со смешанными данными (строки 29-34)"""
        transactions = [
            {"id": 1, "operationAmount": {"currency": {"code": "USD"}}},
            {"id": 2, "operationAmount": {}},
            {"id": 3, "operationAmount": {"currency": {"code": "USD"}}},
            {"id": 4, "operationAmount": "invalid"},
            {"id": 5, "operationAmount": {"currency": {}}},
        ]
        result = list(filter_by_currency(transactions, "USD"))
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 3


# ==================== ТЕСТЫ ДЛЯ transaction_descriptions ====================


class TestTransactionDescriptions:
    """Класс тестов для функции transaction_descriptions"""

    def test_transaction_descriptions_valid(self):
        """Тест получения описаний транзакций (строки 42-43)"""
        transactions = [
            {"description": "Payment 1"},
            {"description": "Payment 2"},
            {"description": "Payment 3"},
        ]
        result = list(transaction_descriptions(transactions))
        assert result == ["Payment 1", "Payment 2", "Payment 3"]

    def test_transaction_descriptions_empty(self, empty_transactions):
        """Тест с пустым списком"""
        result = list(transaction_descriptions(empty_transactions))
        assert result == []

    def test_transaction_descriptions_missing_key(self):
        """Тест с отсутствующим ключом description"""
        transactions = [
            {"description": "Payment 1"},
            {"id": 2},
            {"description": ""},
            {"description": "Payment 2"},
            {"description": None},
        ]
        result = list(transaction_descriptions(transactions))
        assert "Payment 1" in result
        assert "Payment 2" in result
        assert "" not in result
        assert None not in result


# ==================== ТЕСТЫ ДЛЯ card_number_generator ====================


class TestCardNumberGenerator:
    """Класс тестов для генератора card_number_generator"""

    @pytest.mark.parametrize(
        "start, end, expected_count",
        [
            (1, 5, 5),
            (10, 15, 6),
            (100, 105, 6),
            (1, 1, 1),
            (5, 5, 1),
        ],
    )
    def test_card_number_generator_range(self, start, end, expected_count):
        """Тест генерации номеров карт в диапазоне (строки 52-58)"""
        gen = card_number_generator(start, end)
        result = list(gen)
        assert len(result) == expected_count
        for card in result:
            assert isinstance(card, int)
            assert len(str(card)) == 16

    @pytest.mark.parametrize(
        "start, end",
        [
            (10, 5),  # start > end
            (0, 5),  # start = 0
            (-5, -1),  # отрицательные числа
        ],
    )
    def test_card_number_generator_invalid_range(self, start, end):
        """Тест с невалидными диапазонами"""
        gen = card_number_generator(start, end)
        result = list(gen)
        assert result == []

    def test_card_number_generator_format(self):
        """Тест форматирования номеров карт"""
        gen = card_number_generator(1, 3)
        result = list(gen)
        for card in result:
            card_str = str(card)
            assert len(card_str) == 16
            assert card_str.isdigit()

    def test_card_number_generator_uniqueness(self):
        """Тест уникальности генерируемых номеров"""
        gen = card_number_generator(1, 10)
        result = list(gen)
        assert len(result) == len(set(result))

    def test_card_number_generator_sequential(self):
        """Тест последовательной генерации номеров"""
        gen = card_number_generator(1, 5)
        result = list(gen)
        for i in range(len(result) - 1):
            assert result[i + 1] - result[i] == 1


# ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ====================


class TestGeneratorsIntegration:
    """Интеграционные тесты для всех генераторов"""

    def test_filter_and_describe(self):
        """Тест комбинации фильтрации и получения описаний"""
        transactions = [
            {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "Payment"},
            {"id": 2, "operationAmount": {"currency": {"code": "EUR"}}, "description": "Transfer"},
            {"id": 3, "operationAmount": {"currency": {"code": "USD"}}, "description": "Purchase"},
        ]
        filtered = list(filter_by_currency(transactions, "USD"))
        assert len(filtered) == 2
        descriptions = list(transaction_descriptions(filtered))
        assert descriptions == ["Payment", "Purchase"]

    def test_all_generators_together(self):
        """Тест всех генераторов вместе"""
        transactions = [
            {"id": 1, "operationAmount": {"currency": {"code": "USD"}}, "description": "A"},
            {"id": 2, "operationAmount": {"currency": {"code": "USD"}}, "description": "B"},
            {"id": 3, "operationAmount": {"currency": {"code": "EUR"}}, "description": "C"},
        ]
        filtered = list(filter_by_currency(transactions, "USD"))
        assert len(filtered) == 2
        desc = list(transaction_descriptions(filtered))
        assert desc == ["A", "B"]
        cards = list(card_number_generator(1, 3))
        assert len(cards) == 3
        for card in cards:
            assert len(str(card)) == 16
