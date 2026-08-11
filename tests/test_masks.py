import pytest

from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card


class TestMasks:
    @pytest.mark.parametrize(
        "card,expected",
        [
            ("4111111111111111", "411111******1111"),
            ("5500000000000004", "550000******0004"),
            ("378282246310005", "378282******0005"),
            ("1234567890123", "123456******0123"),
            ("9876543210987654321", "987654*********4321"),
            ("4111-1111-1111-1111", "411111******1111"),
            ("5500 0000 0000 0004", "550000******0004"),
        ],
        ids=["visa-16", "mc-16", "amex-15", "min-13", "max-19", "dash", "space"],
    )
    def test_get_mask_card_number_valid(self, card, expected):
        assert get_mask_card_number(card) == expected

    @pytest.mark.parametrize(
        "card",
        ["", None, "123", "abcd", "1" * 3, "4111-abcd-1111-1111"],
        ids=["empty", "none", "too-short", "no-digits", "len-3", "mixed"],
    )
    def test_get_mask_card_number_invalid(self, card):
        with pytest.raises(ValueError):
            get_mask_card_number(card)

    @pytest.mark.parametrize(
        "account,expected",
        [
            ("40817810099910004312", "****************4312"),
            ("30101810200000000700", "****************0700"),
            ("9876543210", "******3210"),
            ("1234", "1234"),
            ("4081-7810-0999-1000-4312", "****************4312"),
        ],
        ids=["acc-20", "acc-another-20", "acc-10", "acc-min", "acc-dash"],
    )
    def test_get_mask_account_valid(self, account, expected):
        assert get_mask_account(account) == expected

    @pytest.mark.parametrize("account", ["", None, "123", "abcd"], ids=["empty", "none", "too-short", "no-digits"])
    def test_get_mask_account_invalid(self, account):
        with pytest.raises(ValueError):
            get_mask_account(account)

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("4111111111111111", "411111******1111"),  # карта
            ("40817810099910004312", "****************4312"),  # счёт
            ("4111-1111-1111-1111", "411111******1111"),  # карта с разделителями
            ("4081-7810-0999-1000-4312", "****************4312"),  # счёт с разделителями
        ],
        ids=["card-16", "acc-20", "card-dash", "acc-dash"],
    )
    def test_mask_account_card_valid(self, value, expected):
        assert mask_account_card(value) == expected

    @pytest.mark.parametrize(
        "value",
        ["", None, "123", "abcd", "text with no numbers"],
        ids=["empty", "none", "too-short", "no-digits", "text-only"],
    )
    def test_mask_account_card_invalid(self, value):
        with pytest.raises(ValueError):
            mask_account_card(value)


from src.masks import get_mask_account, get_mask_card_number, mask_account_card


class TestMasks:
    def test_get_mask_card_number_valid(self, valid_card_cases):
        for value, expected in valid_card_cases:
            assert get_mask_card_number(value) == expected

    def test_get_mask_card_number_separators(self, card_with_separators):
        for value, expected in card_with_separators:
            assert get_mask_card_number(value) == expected

    def test_get_mask_card_number_invalid_raises(self, invalid_card_input):
        with pytest.raises(ValueError):
            get_mask_card_number(invalid_card_input)

    def test_get_mask_account_valid(self, valid_account_cases):
        for value, expected in valid_account_cases:
            assert get_mask_account(value) == expected

    def test_get_mask_account_invalid_raises(self, invalid_account_input):
        with pytest.raises(ValueError):
            get_mask_account(invalid_account_input)

    def test_mask_account_card_valid(self, card_or_account_case):
        value, expected = card_or_account_case
        assert mask_account_card(value) == expected

    def test_mask_account_card_invalid_raises(self, invalid_card_or_account_input):
        with pytest.raises(ValueError):
            mask_account_card(invalid_card_or_account_input)



            from masks import get_mask_card_number

            @pytest.mark.parametrize(
                "card_number,expected_error",
                [
                    (None, ValueError),
                    ("", ValueError),
                    ("   ", ValueError),
                    ("123", ValueError),  # если по логике нужен минимум 16
                ],
            )
            def test_get_mask_card_number_invalid(card_number, expected_error):
                with pytest.raises(expected_error):
                    get_mask_card_number(card_number)

            def test_get_mask_card_number_valid():
                assert get_mask_card_number("1234567890123456") == "**** **** **** 3456"

