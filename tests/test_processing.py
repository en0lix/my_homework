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
    assert len(result) == 3
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


# ===== ТЕСТЫ ДЛЯ sort_by_date =====

def test_sort_by_date_descending(sample_transactions):
    """Тест сортировки по убыванию (новые → старые)"""
    result = sort_by_date(sample_transactions, reverse=True)
    dates = [item["date"] for item in result]
    expected = sorted(dates, reverse=True)
    assert dates == expected


def test_sort_by_date_ascending(sample_transactions):
    """Тест сортировки по возрастанию (старые → новые)"""
    result = sort_by_date(sample_transactions, reverse=False)
    dates = [item["date"] for item in result]
    expected = sorted(dates)
    assert dates == expected


def test_sort_by_date_default(sample_transactions):
    """Тест сортировки с параметром по умолчанию (по убыванию)"""
    result = sort_by_date(sample_transactions)
    dates = [item["date"] for item in result]
    expected = sorted(dates, reverse=True)
    assert dates == expected


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


def test_sort_by_date_missing_key():
    """Тест с отсутствующим ключом date"""
    transactions = [
        {"id": 1},
        {"id": 2, "date": "2026-08-22T10:00:00"},
        {"id": 3},
    ]
    result = sort_by_date(transactions)
    # Транзакции без даты должны быть в конце списка
    assert len(result) == 3
    # Последние элементы должны быть без даты
    assert result[0]["id"] == 2  # С датой должна быть первой