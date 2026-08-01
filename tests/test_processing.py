import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    def test_filter_by_each_state_count(self, base_records, state_and_count):
        state, expected_count = state_and_count
        result = filter_by_state(base_records, state)
        assert len(result) == expected_count
        if expected_count > 0:
            assert all(r.get("state") == state for r in result)

    def test_no_records_with_state_return_empty(self, base_records, absent_state):
        result = filter_by_state(base_records, absent_state)
        assert result == []

    def test_empty_records_list_returns_empty(self):
        assert filter_by_state([], "new") == []

    def test_records_without_state_key_are_ignored(self, base_records):
        result = filter_by_state(base_records, "new")
        assert len(result) == 3
        assert all(r.get("state") == "new" for r in result)


class TestSortByDate:
    def test_sort_ascending(self, base_records):
        sorted_asc = sort_by_date(base_records, reverse=False)
        dates = [r.get("date") for r in sorted_asc]
        # Фильтруем None и проверяем, что валидные даты по возрастанию
        valid_dates = [d for d in dates if d is not None]
        assert valid_dates == sorted(valid_dates)

    def test_sort_descending(self, base_records):
        sorted_desc = sort_by_date(base_records, reverse=True)
        dates = [r.get("date") for r in sorted_desc]
        valid_dates = [d for d in dates if d is not None]
        assert valid_dates == sorted(valid_dates, reverse=True)

    def test_same_dates_order_stable(self, base_records):
        # В
        import pytest

        from src.processing import filter_by_state

        class TestFilterByState:
            def test_filter_by_each_state_count(self, base_records, state_and_count):
                state, expected_count = state_and_count
                result = filter_by_state(base_records, state)
                assert len(result) == expected_count
                if expected_count > 0:
                    assert all(r["state"] == state for r in result)

            def test_no_records_with_state_return_empty(self, base_records, absent_state):
                result = filter_by_state(base_records, absent_state)
                assert result == []

            def test_empty_records_list_returns_empty(self):
                assert filter_by_state([], "new") == []

            def test_records_without_state_key_are_ignored(self, base_records):
                result = filter_by_state(base_records, "new")
                assert len(result) == 2
                assert all(r["state"] == "new" for r in result)
