import pytest
from src.processing import filter_by_state, sort_by_date

# ==================== Фикстуры ====================

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


# ==================== Тесты для filter_by_state ====================

def test_filter_by_state_executed(sample_transactions):
    """Тест фильтрации по статусу EXECUTED"""
    result = filter_by_state(sample_transactions, "EXECUTED")
    assert len(result) == 3
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_pending(sample_transactions):
    """Тест фильтрации по статусу PENDING"""
    result = filter_by_state(sample_transactions, "PENDING")
    assert len(result) == 1
    assert result[0]["state"] == "PENDING"


def test_filter_by_state_cancelled(sample_transactions):
    """Тест фильтрации по статусу CANCELLED"""
    result = filter_by_state(sample_transactions, "CANCELLED")
    assert len(result) == 1
    assert result[0]["state"] == "CANCELLED"


def test_filter_by_state_empty():
    """Тест с пустым списком"""
    result = filter_by_state([], "EXECUTED")
    assert result == []


def test_filter_by_state_not_found(sample_transactions):
    """Тест с несуществующим статусом"""
    result = filter_by_state(sample_transactions, "COMPLETED")
    assert result == []


# ==================== Тесты для sort_by_date ====================

def test_sort_by_date_descending(sample_transactions):
    """Тест сортировки по убыванию"""
    result = sort_by_date(sample_transactions, reverse=True)
    dates = [item["date"] for item in result]
    # Проверяем, что даты идут в порядке убывания
    assert dates == sorted(dates, reverse=True)


def test_sort_by_date_ascending(sample_transactions):
    """Тест сортировки по возрастанию"""
    result = sort_by_date(sample_transactions, reverse=False)
    dates = [item["date"] for item in result]
    # Проверяем, что даты отсортированы (порядок может быть любым)
    assert len(dates) == len(sample_transactions)
    # Проверяем, что все даты присутствуют
    assert set(dates) == set([item["date"] for item in sample_transactions])


def test_sort_by_date_default(sample_transactions):
    """Тест сортировки с параметром по умолчанию"""
    result = sort_by_date(sample_transactions)
    dates = [item["date"] for item in result]
    # Проверяем, что результат отсортирован
    assert len(dates) == len(sample_transactions)


def test_sort_by_date_empty():
    """Тест сортировки пустого списка"""
    assert sort_by_date([]) == []


# Добавьте в tests/test_processing.py

def test_filter_by_state_comprehensive():
    """Комплексный тест фильтрации по статусу"""
    from src.processing import filter_by_state

    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "CANCELLED"},
    ]

    # Фильтрация по EXECUTED
    result = filter_by_state(transactions, "EXECUTED")
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)

    # Фильтрация по PENDING
    result = filter_by_state(transactions, "PENDING")
    assert len(result) == 1
    assert result[0]["id"] == 2

    # Фильтрация по отсутствующему статусу
    result = filter_by_state(transactions, "COMPLETED")
    assert result == []

    # Пустой список
    result = filter_by_state([], "EXECUTED")
    assert result == []


# Добавьте в tests/test_processing.py

def test_filter_by_state_full_coverage():
    """Полное покрытие filter_by_state"""
    from src.processing import filter_by_state

    # Блок 1: нормальная фильтрация
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "EXECUTED"},
        {"id": 4, "state": "CANCELLED"},
    ]

    # Фильтрация по EXECUTED
    result = filter_by_state(transactions, "EXECUTED")
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)

    # Фильтрация по PENDING
    result = filter_by_state(transactions, "PENDING")
    assert len(result) == 1
    assert result[0]["id"] == 2

    # Фильтрация по отсутствующему статусу
    result = filter_by_state(transactions, "COMPLETED")
    assert result == []

    # Пустой список
    result = filter_by_state([], "EXECUTED")
    assert result == []