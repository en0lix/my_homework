"""Тесты для функций process_bank_search и process_bank_operations."""

import pytest

from src.utils import process_bank_operations, process_bank_search


class TestProcessBankSearch:
    """Тесты для process_bank_search."""

    @pytest.fixture
    def transactions(self) -> list:
        return [
            {"description": "Перевод организации"},
            {"description": "Открытие вклада"},
            {"description": "Перевод с карты на карту"},
            {"description": "Пополнение счета"},
        ]

    def test_search_by_word(self, transactions: list) -> None:
        """Поиск по слову 'Перевод'."""
        result = process_bank_search(transactions, "Перевод")
        assert len(result) == 2

    def test_search_case_insensitive(self, transactions: list) -> None:
        """Поиск без учёта регистра."""
        result = process_bank_search(transactions, "ПЕРЕВОД")
        assert len(result) == 2

    def test_search_empty_string(self, transactions: list) -> None:
        """Пустой запрос — пустой результат."""
        assert process_bank_search(transactions, "") == []

    def test_search_no_matches(self, transactions: list) -> None:
        """Ничего не найдено."""
        assert process_bank_search(transactions, "Ипотека") == []

    def test_search_with_special_chars(self, transactions: list) -> None:
        """Спецсимволы не должны ломать регулярку."""
        result = process_bank_search(transactions, ".(*)")
        assert result == []


class TestProcessBankOperations:
    """Тесты для process_bank_operations."""

    @pytest.fixture
    def transactions(self) -> list:
        return [
            {"description": "Перевод организации"},
            {"description": "Перевод организации"},
            {"description": "Открытие вклада"},
            {"description": "Перевод с карты на карту"},
        ]

    def test_count_categories(self, transactions: list) -> None:
        """Подсчёт по категориям."""
        result = process_bank_operations(
            transactions,
            ["Перевод организации", "Открытие вклада", "Перевод с карты на карту"],
        )
        assert result["Перевод организации"] == 2
        assert result["Открытие вклада"] == 1
        assert result["Перевод с карты на карту"] == 1

    def test_missing_categories(self, transactions: list) -> None:
        """Категории, которых нет — 0."""
        result = process_bank_operations(transactions, ["Ипотека"])
        assert result == {"Ипотека": 0}

    def test_empty_data(self) -> None:
        """Пустой список транзакций."""
        assert process_bank_operations([], ["Перевод"]) == {"Перевод": 0}