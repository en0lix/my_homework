import pytest
from src.widget import format_widget, validate_widget_data  # имена подставь свои

@pytest.mark.parametrize(
    "input_data,expected",
    [
        ({"id": 1, "name": "Test"}, "Widget #1: Test"),
        ({"id": 2, "name": "Demo"}, "Widget #2: Demo"),
    ],
)
def test_format_widget(input_data, expected):
    assert format_widget(input_data) == expected


@pytest.mark.parametrize(
    "data,raises_error",
    [
        ({}, True),
        ({"name": "No ID"}, True),
        ({"id": -1, "name": "Invalid"}, True),
        ({"id": 3, "name": "Valid"}, False),
    ],
)
def test_validate_widget_data(data, raises_error):
    if raises_error:
        with pytest.raises(ValueError):
            validate_widget_data(data)
    else:
        # Если функция ничего не возвращает, то достаточно, что она не кидает ошибку
        validate_widget_data(data)
