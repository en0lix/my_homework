import pytest

from widget import mask_account_card


@pytest.mark.parametrize(
    "input_value,expected_type,expected_result",
    [
        # Карта: 16 цифр → маска карты
        ("4111111111111111", "card", "4111 11** **** 1111"),
        # Счет: длинная строка цифр → маска счета
        ("12345678901234567890", "account", "12** ************7890"),
        # Строка с текстом и цифрами (распознаем тип по содержимому)
        ("Счет №12345678901234567890", "account", "12** ************7890"),
        ("Карта 4111111111111111", "card", "4111 11** **** 1111"),
        # Короткие/некорректные данные: должно падать с ValueError
        ("123", None, None),
        ("", None, None),
        (None, None, None),
    ],
    ids=[
        "card_16_digits",
        "account_long_number",
        "account_with_prefix",
        "card_with_prefix",
        "short_invalid",
        "empty_string",
        "none_input",
    ],
)
def test_mask_account_card(input_value, expected_type, expected_result):
    if expected_result is None:
        # Для некорректных входных данных ожидаем ошибку
        with pytest.raises(ValueError):
            mask_account_card(input_value)
    else:
        result = mask_account_card(input_value)
        assert result == expected_result

        import pytest

        from widget import get_date

        @pytest.mark.parametrize(
            "input_str,expected_output",
            [
                ("2024-01-15", "2024-01-15"),
                ("15.01.2024", "2024-01-15"),
                ("01/15/2024", "2024-01-15"),
                ("15 января 2024", "2024-01-15"),  # если функция поддерживает слова
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
                "text_month",
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
