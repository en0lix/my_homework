import pytest

from src.dates import get_date


class TestGetDate:
    def test_valid_formats_normalized(self, valid_date_pair):
        inp, expected = valid_date_pair
        assert get_date(inp) == expected

    @pytest.mark.parametrize(
        "inp,expected",
        [
            ("2023-12-31", "2023-12-31"),
            ("2024-01-01", "2024-01-01"),
            ("2024-02-29", "2024-02-29"),
            ("2023-02-28", "2023-02-28"),
        ],
        ids=["year-end", "year-start", "leap-day", "feb-last"],
    )
    def test_boundary_dates(self, inp, expected):
        assert get_date(inp) == expected

    def test_invalid_raises_value_error(self, invalid_date_input):
        with pytest.raises(ValueError):
            get_date(invalid_date_input)

    def test_none_empty_whitespace_return_empty(self):
        assert get_date("") == ""
        assert get_date(None) == ""
        assert get_date("   ") == ""
