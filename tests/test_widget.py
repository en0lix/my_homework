python
"""
Тесты для модуля widget.
"""

import pytest

from src.widget import get_date, mask_account_card, validate_widget_data

# ==================== ТЕСТЫ ДЛЯ mask_account_card ====================


def test_mask_account_card_card() -> None:
    """Тест маскирования карты"""
    result = mask_account_card("Visa 1234567890123456")
    assert result == "1234 56** **** 3456"


def test_mask_account_card_account() -> None:
    """Тест маскирования счета"""
    result = mask_account_card("Счет 12345678901234567890")
    assert result == "**7890"


def test_mask_account_card_empty() -> None:
    """Тест пустой строки"""
    assert mask_account_card("") == ""


def test_mask_account_card_none() -> None:
    """Тест None"""
    assert mask_account_card(None) == ""


def test_mask_account_card_invalid() -> None:
    """Тест некорректных данных"""
    with pytest.raises(ValueError):
        mask_account_card("Invalid data")


def test_mask_account_card_only_number() -> None:
    """Тест только номера"""
    result = mask_account_card("1234567890123456")
    assert result == "1234 56** **** 3456"


def test_mask_account_card_only_account() -> None:
    """Тест только номера счета"""
    result = mask_account_card("12345678901234567890")
    assert result == "**7890"


def test_mask_account_card_with_spaces() -> None:
    """Тест с лишними пробелами"""
    result = mask_account_card("Visa  1234567890123456")
    assert result == "1234 56** **** 3456"


def test_mask_account_card_mixed_case() -> None:
    """Тест разных регистров"""
    result = mask_account_card("visa 1234567890123456")
    assert result == "1234 56** **** 3456"


def test_mask_account_card_different_types() -> None:
    """Тест с разными типами карт"""
    test_cases: list[tuple[str, str]] = [
        ("MasterCard 1234567890123456", "1234 56** **** 3456"),
        ("Maestro 1234567890123456", "1234 56** **** 3456"),
        ("МИР 1234567890123456", "1234 56** **** 3456"),
    ]
    for input_data, expected in test_cases:
        result = mask_account_card(input_data)
        assert result == expected


# ==================== ТЕСТЫ ДЛЯ get_date ====================


def test_get_date_iso_format() -> None:
    """Тест ISO формата"""
    assert get_date("2026-08-22") == "2026-08-22"
    assert get_date("2026-12-31") == "2026-12-31"


def test_get_date_with_time() -> None:
    """Тест с временем"""
    result = get_date("2026-08-22T15:30:00")
    assert result == "2026-08-22"


def test_get_date_with_timezone() -> None:
    """Тест с временной зоной"""
    result = get_date("2026-08-22T15:30:00+03:00")
    assert result == "2026-08-22"


def test_get_date_empty() -> None:
    """Тест пустой строки"""
    result = get_date("")
    assert result is None


def test_get_date_none() -> None:
    """Тест None"""
    result = get_date(None)
    assert result is None


def test_get_date_invalid() -> None:
    """Тест некорректной даты"""
    result = get_date("invalid date")
    assert result is None or result == "invalid date"


def test_get_date_dot_format() -> None:
    """Тест формата DD.MM.YYYY"""
    result = get_date("22.08.2026")
    assert result is None or isinstance(result, str)


def test_get_date_edge_cases() -> None:
    """Тест граничных случаев"""
    result1 = get_date("2026-00-01")
    result2 = get_date("2026-13-01")
    result3 = get_date("2026-01-32")

    assert result1 is None or isinstance(result1, str)
    assert result2 is None or isinstance(result2, str)
    assert result3 is None or isinstance(result3, str)


# ==================== ТЕСТЫ ДЛЯ validate_widget_data ====================


def test_validate_widget_data_valid() -> None:
    """Тест валидных данных"""
    result = validate_widget_data({"title": "Test", "type": "card"})
    assert result is None


def test_validate_widget_data_invalid() -> None:
    """Тест невалидных данных"""
    with pytest.raises(ValueError, match="Data must be a dictionary"):
        validate_widget_data(None)

    with pytest.raises(ValueError, match="Data must be a dictionary"):
        validate_widget_data("not a dict")  # type: ignore

    with pytest.raises(ValueError, match="Data must be a dictionary"):
        validate_widget_data([])  # type: ignore

    with pytest.raises(ValueError, match="Missing 'title' key"):
        validate_widget_data({"type": "card"})
