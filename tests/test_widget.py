import pytest

from src.widget import get_date


@pytest.mark.parametrize(
    "input_str,expected_output",
    [
        ("2024-01-15", "2024-01-15"),
        ("15.01.2024", "2024-01-15"),
        ("01/15/2024", "2024-01-15"),
        ("2024/01/15", "2024-01-15"),
        ("Дата: 2024-02-29", "2024-02-29"),  # высокосный год
        ("Нет даты здесь", None),
        ("", None),
        ("abc123xyz", None),
    ],
    ids=[
        "iso_format",
        "dot_format",
        "slash_format",
        "alt_slash_format",
        "leap_year",
        "no_date_in_text",
        "empty_string",
        "random_string",
    ],
)
def test_get_date(input_str, expected_output):
    result = get_date(input_str)
    assert result == expected_output


import pytest

from src.widget import validate_widget_data


@pytest.mark.parametrize(
    "data,expected_error",
    [
        (None, ValueError),
        ({"title": "", "value": "123"}, ValueError),
        ({"title": "   ", "value": "123"}, ValueError),
        ({"value": "123"}, ValueError),  # нет title
        ({"title": "Price", "value": ""}, ValueError),
    ],
)
def test_validate_widget_data_invalid(data, expected_error):
    with pytest.raises(expected_error):
        validate_widget_data(data)


def test_validate_widget_data_valid():
    data = {"title": "Price", "value": "100"}
    # Если функция ничего не возвращает, достаточно, что она не выбросила ошибку
    validate_widget_data(data)
