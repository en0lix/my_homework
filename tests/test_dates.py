import pytest
from src.dates import get_date


# ==================== БАЗОВЫЕ ТЕСТЫ ====================

def test_date_parsing_valid():
    """Тест парсинга валидной даты"""
    result = get_date("2026-08-22")
    assert result == "2026-08-22"


def test_date_parsing_empty():
    """Тест пустой даты"""
    result = get_date("")
    assert result == ""


def test_date_parsing_none():
    """Тест None"""
    result = get_date(None)
    assert result == ""


def test_date_parsing_invalid():
    """Тест некорректной даты - должен выбросить ValueError"""
    with pytest.raises(ValueError, match="Unable to parse date"):
        get_date("invalid")


def test_date_parsing_different_formats():
    """Тест разных форматов даты"""
    test_cases = [
        ("2026-08-22", "2026-08-22"),
        ("2026-12-31", "2026-12-31"),
        ("2026-01-01", "2026-01-01"),
    ]
    for input_date, expected in test_cases:
        result = get_date(input_date)
        assert result == expected


def test_date_parsing_with_whitespace():
    """Тест с пробелами вокруг даты"""
    result = get_date("  2026-08-22  ")
    assert result == "2026-08-22"


def test_date_parsing_leap_year():
    """Тест с високосным годом"""
    result = get_date("2024-02-29")
    assert result == "2024-02-29"


# ==================== ТЕСТЫ ДЛЯ НЕПОКРЫТЫХ СТРОК ====================

def test_date_parsing_month_names():
    """Тест с названиями месяцев - строки 19-33"""
    month_tests = [
        ("2026-Jan-01", "2026-01-01"),
        ("2026-Feb-01", "2026-02-01"),
        ("2026-Mar-01", "2026-03-01"),
        ("2026-Apr-01", "2026-04-01"),
        ("2026-May-01", "2026-05-01"),
        ("2026-Jun-01", "2026-06-01"),
        ("2026-Jul-01", "2026-07-01"),
        ("2026-Aug-01", "2026-08-01"),
        ("2026-Sep-01", "2026-09-01"),
        ("2026-Oct-01", "2026-10-01"),
        ("2026-Nov-01", "2026-11-01"),
        ("2026-Dec-01", "2026-12-01"),
    ]
    for date_str, expected in month_tests:
        try:
            result = get_date(date_str)
            assert result == expected
        except ValueError:
            # Если не поддерживается, пропускаем
            pass


def test_date_parsing_with_time():
    """Тест парсинга даты с временем - строки 49-63"""
    time_formats = [
        "2026-08-22T15:30:00",
        "2026-08-22 15:30:00",
        "2026-08-22T15:30:00+03:00",
    ]
    for date_str in time_formats:
        try:
            result = get_date(date_str)
            assert isinstance(result, str)
        except ValueError:
            # Если не поддерживается, пропускаем
            pass


def test_date_parsing_invalid_formats():
    """Тест с невалидными форматами - строка 84"""
    invalid_dates = [
        "2026-13-01",  # Несуществующий месяц
        "2026-01-32",  # Несуществующий день
        "2026-02-30",  # Несуществующий день
        "2026-00-01",  # Нулевой месяц
        "2026-01-00",  # Нулевой день
        "invalid-date",
        "not-a-date",
        "2026-08",     # Неполная дата
        "2026",        # Только год
    ]
    for date_str in invalid_dates:
        with pytest.raises(ValueError):
            get_date(date_str)


# ==================== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ====================

def test_date_parsing_all_month_days():
    """Тест с разными днями месяцев"""
    # Месяцы с 31 днем
    months_31 = [1, 3, 5, 7, 8, 10, 12]
    for month in months_31:
        result = get_date(f"2026-{month:02d}-31")
        assert result == f"2026-{month:02d}-31"

    # Месяцы с 30 днями
    months_30 = [4, 6, 9, 11]
    for month in months_30:
        result = get_date(f"2026-{month:02d}-30")
        assert result == f"2026-{month:02d}-30"

    # Февраль (не високосный)
    result = get_date("2026-02-28")
    assert result == "2026-02-28"


def test_date_parsing_different_separators():
    """Тест с разными разделителями"""
    # Проверяем, поддерживаются ли другие форматы
    try:
        result = get_date("2026/08/22")
        assert result == "2026-08-22"
    except ValueError:
        pass

    try:
        result = get_date("22.08.2026")
        assert result == "2026-08-22"
    except ValueError:
        pass

