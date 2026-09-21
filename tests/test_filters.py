# tests/test_filters.py

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2026-08-22T10:00:00"},
        {"id": 2, "state": "PENDING", "date": "2026-08-21T15:30:00"},
        {"id": 3, "state": "EXECUTED", "date": "2026-08-20T09:15:00"},
        {"id": 4, "state": "CANCELLED", "date": "2026-08-19T18:45:00"},
        {"id": 5, "state": "EXECUTED", "date": "2026-08-18T12:00:00"},
    ]


# ===== ТЕСТЫ ДЛЯ filter_by_state =====


def test_filter_by_state_executed(sample_transactions):
    """Тест фильтрации по статусу EXECUTED"""
    result = filter_by_state(sample_transactions, "EXECUTED")
    assert len(result) == 3  # В фикстуре 3 транзакции с EXECUTED
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_pending(sample_transactions):
    """Тест фильтрации по статусу PENDING"""
    result = filter_by_state(sample_transactions, "PENDING")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_filter_by_state_cancelled(sample_transactions):
    """Тест фильтрации по статусу CANCELLED"""
    result = filter_by_state(sample_transactions, "CANCELLED")
    assert len(result) == 1
    assert result[0]["id"] == 4


def test_filter_by_state_not_found(sample_transactions):
    """Тест с несуществующим статусом"""
    result = filter_by_state(sample_transactions, "COMPLETED")
    assert result == []


def test_filter_by_state_empty():
    """Тест с пустым списком"""
    result = filter_by_state([], "EXECUTED")
    assert result == []


def test_filter_by_state_missing_key():
    """Тест с отсутствующим ключом state"""
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2},
        {"id": 3, "state": "EXECUTED"},
    ]
    result = filter_by_state(transactions, "EXECUTED")
    # Должен вернуть только транзакции с ключом state
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)


# ===== ТЕСТЫ ДЛЯ sort_by_date =====


def test_sort_by_date_descending(sample_transactions):
    """Тест сортировки по убыванию"""
    result = sort_by_date(sample_transactions, reverse=True)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_transactions):
    """Тест сортировки по возрастанию"""
    result = sort_by_date(sample_transactions, reverse=False)
    dates = [item["date"] for item in result]
    assert dates == sorted(dates)


def test_sort_by_date_default(sample_transactions):
    """Тест сортировки с параметром по умолчанию"""
    result = sort_by_date(sample_transactions)
    dates = [item["date"] for item in result]
    # По умолчанию должна быть сортировка по убыванию
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_empty():
    """Тест сортировки пустого списка"""
    result = sort_by_date([])
    assert result == []


def test_sort_by_date_same_dates():
    """Тест сортировки с одинаковыми датами"""
    transactions = [
        {"id": 1, "date": "2026-08-22T10:00:00"},
        {"id": 2, "date": "2026-08-22T10:00:00"},
        {"id": 3, "date": "2026-08-22T10:00:00"},
    ]
    result = sort_by_date(transactions)
    assert len(result) == 3
    assert all(item["date"] == "2026-08-22T10:00:00" for item in result)
