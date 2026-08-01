from datetime import date

import pytest


@pytest.fixture
def base_records():
    """Набор записей с разными state и датами, включая граничные случаи."""
    return [
        {"id": 1, "state": "new", "date": "2024-01-10"},
        {"id": 2, "state": "pending", "date": "2024-01-05"},
        {"id": 3, "state": "done", "date": "2024-01-12"},
        {"id": 4, "state": "new", "date": "2024-01-08"},
        {"id": 5, "state": "failed", "date": "2024-01-07"},
        {"id": 6, "date": "2024-01-06"},  # нет state
        {"id": 7, "state": None, "date": "2024-01-09"},  # state=None
        {"id": 8, "state": "new", "date": "2024-01-08"},  # дубликат даты
    ]


@pytest.fixture(
    params=[
        ("new", 3),
        ("pending", 1),
        ("done", 1),
        ("failed", 1),
        ("unknown", 0),
    ],
    ids=[
        "filter-new",
        "filter-pending",
        "filter-done",
        "filter-failed",
        "filter-unknown-empty",
    ],
)
def state_and_count(request):
    return request.param


@pytest.fixture(
    params=["unknown", "cancelled", "archived"],
    ids=[
        "absent-unknown",
        "absent-cancelled",
        "absent-archived",
    ],
)
def absent_state(request):
    return request.param


@pytest.fixture(
    params=[
        ("2024-01-15", "2024-01-15"),
        ("15/01/2024", "2024-01-15"),
        ("01.15.2024", "2024-01-15"),
        ("Jan 15, 2024", "2024-01-15"),
        ("2024/01/15", "2024-01-15"),
    ],
    ids=[
        "iso",
        "dd-mm-yyyy",
        "mm-dd-yyyy",
        "month-name",
        "slash-year-first",
    ],
)
def valid_date_pair(request):
    return request.param


@pytest.fixture(
    params=[
        "",
        None,
        "   ",
        "no date here",
        "2024-13-01",
        "2024-01-32",
        "text with 2024-01-15 extra words",
    ],
    ids=[
        "empty",
        "none",
        "whitespace",
        "text-no-date",
        "invalid-month",
        "invalid-day",
        "date-in-text",
    ],
)
def invalid_date_input(request):
    return request.param


from typing import Any, Dict, List, Tuple

import pytest


# -------------------------
# Фикстуры для масок карт
# -------------------------
@pytest.fixture
def valid_card_cases() -> List[Tuple[str, str]]:
    return [
        ("4111111111111111", "411111******1111"),
        ("5500000000000004", "550000******0004"),
        ("378282246310005", "378282******0005"),
        ("1234567890123", "123456******0123"),
        ("9876543210987654321", "987654*********4321"),
    ]


@pytest.fixture
def card_with_separators() -> List[Tuple[str, str]]:
    return [
        ("4111-1111-1111-1111", "411111******1111"),
        ("5500 0000 0000 0004", "550000******0004"),
    ]


@pytest.fixture(
    params=[
        "",
        None,
        "123",
        "1" * 12,
        "1" * 20,
        "abcd",
    ],
    ids=[
        "empty",
        "none",
        "too-short",
        "just-under-min",
        "over-max",
        "no-digits",
    ],
)
def invalid_card_input(request):
    return request.param


# -------------------------
# Фикстуры для масок счетов
# -------------------------
@pytest.fixture
def valid_account_cases() -> List[Tuple[str, str]]:
    return [
        ("40817810099910004312", "****************4312"),
        ("9876543210", "******3210"),
        ("00001111", "****1111"),
        ("1234", "1234"),
    ]


@pytest.fixture(
    params=[
        "",
        None,
        "123",
        "abcd",
    ],
    ids=["empty", "none", "too-short", "no-digits"],
)
def invalid_account_input(request):
    return request.param


# -------------------------
# Фикстуры для mask_account_card
# -------------------------
@pytest.fixture(
    params=[
        ("4111111111111111", "411111******1111"),  # карта
        ("40817810099910004312", "****************4312"),  # счёт
        ("9876543210", "******3210"),  # счёт (не карта)
    ],
    ids=["card-16", "acc-20", "acc-10"],
)
def card_or_account_case(request):
    return request.param


@pytest.fixture(
    params=["", None, "123", "abcd", "text with 123"], ids=["empty", "none", "short", "no-digits", "mixed"]
)
def invalid_card_or_account_input(request):
    return request.param


# -------------------------
# Фикстуры для get_date
# -------------------------
@pytest.fixture(
    params=[
        ("2024-01-15", "2024-01-15"),
        ("15/01/2024", "2024-01-15"),
        ("01.15.2024", "2024-01-15"),
        ("Jan 15, 2024", "2024-01-15"),
    ],
    ids=["iso", "dd-mm", "mm-dd", "month-name"],
)
def valid_date_case(request):
    return request.param


@pytest.fixture(
    params=[
        ("",),
        (None,),
        ("   ",),
        ("no date",),
        ("2024-13-01",),
    ],
    ids=["empty", "none", "spaces", "text", "bad-month"],
)
def invalid_date_input(request):
    return request.param[0] if isinstance(request.param, tuple) else request.param


# -------------------------
# Фикстуры для filter_by_state
# -------------------------
@pytest.fixture
def base_records() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "state": "new", "date": "2024-01-10"},
        {"id": 2, "state": "pending", "date": "2024-01-05"},
        {"id": 3, "state": "done", "date": "2024-01-12"},
        {"id": 4, "state": "new", "date": "2024-01-08"},
        {"id": 5, "state": "failed", "date": "2024-01-07"},
        {"id": 6, "date": "2024-01-06"},  # нет state
        {"id": 7, "state": None, "date": "2024-01-09"},  # state == None
    ]


@pytest.fixture(
    params=[
        ("new", 2),
        ("pending", 1),
        ("done", 1),
        ("failed", 1),
        ("unknown", 0),
    ],
    ids=["new", "pending", "done", "failed", "unknown"],
)
def state_and_count(request):
    return request.param


@pytest.fixture(params=["unknown", "cancelled", "archived"], ids=["unk", "can", "arc"])
def absent_state(request):
    return request.param
