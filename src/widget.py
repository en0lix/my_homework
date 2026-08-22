# src/widget.py
def validate_widget_data(data):
    # Пример простой валидации: проверяем, что есть обязательные поля
    required_keys = {"id", "name", "value"}
    if not isinstance(data, dict):
        return False
    return required_keys.issubset(data.keys())


def get_date(date: str) -> str:
    """Функция преобразует дату в формат 'DD.MM.YYYY'"""
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    return date.strftime("%d.%m.%Y")


def get_mask_account_card(account_card: str) -> str:
    """
    Принимает один аргумент — строку, содержащую тип и номер карты или счета,
     и возвращает строку с замаскированным номером.
    """
    if "Счет" in account_card:
        letters_count = "".join(re.findall(r"\D+", account_card))
        numbers_count = "".join(re.findall(r"\d+", account_card))
        return f"{letters_count} {get_mask_account(numbers_count)}"
    else:
        letters_card = "".join(re.findall(r"\D+", account_card))
        numbers_card = "".join(re.findall(r"\d+", account_card))
        return f"{letters_card} {get_mask_card_number(numbers_card)}"


from typing import Optional


def mask_account_card(value: Optional[str]) -> str:
    """
    Универсальная маска: если похоже на карту (13–19 цифр) — маска карты,
    иначе если >= 4 цифр — маска счёта, иначе ValueError.
    None/пустая строка → "".
    """
    if value is None or value == "":
        return ""

    digits = "".join(ch for ch in str(value) if ch.isdigit())

    if 13 <= len(digits) <= 19:
        return get_mask_card_number(value)

    if len(digits) >= 4:
        return get_mask_account(value)

    raise ValueError("Cannot determine mask type: not a valid card or account")


import re
from datetime import datetime
from typing import Optional

DATE_FORMATS = [
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d",
    "%d.%m.%Y",
    "%m/%d/%Y",
    "%Y/%m/%d",
    "%b %d, %Y",
]

DATE_PATTERN = re.compile(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[./]\d{1,2}[./]\d{4}")


def get_date(date_str: Optional[str]) -> Optional[str]:
    if date_str is None or date_str == "" or (isinstance(date_str, str) and date_str.strip() == ""):
        return None

    date_str = str(date_str).strip()

    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    match = DATE_PATTERN.search(date_str)
    if match:
        for fmt in DATE_FORMATS:
            try:
                dt = datetime.strptime(match.group(), fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

    return None


def validate_widget_data(data) -> None:
    if data is None or not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")
    if "title" not in data:
        raise ValueError("Missing 'title' key")
    if not isinstance(data["title"], str) or data["title"].strip() == "":
        raise ValueError("Title cannot be empty")
    if "value" not in data:
        raise ValueError("Missing 'value' key")
    if not isinstance(data["value"], str) or data["value"] == "":
        raise ValueError("Value cannot be empty")


import pytest
from src.masks import get_mask_card_number, get_mask_account

@pytest.mark.parametrize(
    "value, expected_type_hint, expected_result_contains",
    [
        # Карта: должно применяться маскирование карты
        ("1234567890123456", "card", "************3456"),
        ("4111 1111 1111 1111", "card", "************1111"),
        # Счёт: должно применяться маскирование счёта
        ("11112222333344445555", "account", "****************5555"),
        ("40817-810-0-0000-0000001", "account", "***************0001"),
    ],
)
def test_mask_account_card_universal(value, expected_type_hint, expected_result_contains):
    result = mask_account_card(value)
    # Проверяем, что результат содержит ожидаемую маску
    assert expected_result_contains in result


@pytest.mark.parametrize("value", [None, "", "   ", "abc", "12a34"])
def test_mask_account_card_invalid(value):
    with pytest.raises(ValueError):
        mask_account_card(value)


@pytest.mark.parametrize(
    "date_input, expected",
    [
        ("2024-01-15", "15.01.2024"),
        ("2024/01/15", "15.01.2024"),
        ("15.01.2024", "15.01.2024"),
        ("2024-12-31", "31.12.2024"),
    ],
)
def test_get_date_valid(date_input, expected):
    assert get_date(date_input) == expected


@pytest.mark.parametrize(
    "date_input",
    [None, "", "   ", "abc", "2024-13-01", "2024-02-30", "32.01.2024"],
)
def test_get_date_invalid(date_input):
    with pytest.raises(ValueError):
        get_date(date_input)

