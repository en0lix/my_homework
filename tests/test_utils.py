"""
Тесты для модуля utils.
"""

import json
import os
import tempfile

import pytest

from src.utils import get_transactions_from_json


class TestGetTransactionsFromJson:
    """Тесты для функции get_transactions_from_json."""

    def test_valid_json_file(self) -> None:
        """Тест чтения валидного JSON-файла."""
        test_data = [
            {"id": 1, "state": "EXECUTED", "amount": 100},
            {"id": 2, "state": "PENDING", "amount": 200},
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            json.dump(test_data, tmp_file)
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_json(tmp_file_path)
            assert result == test_data
            assert isinstance(result, list)
            assert len(result) == 2
        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_empty_json_file(self) -> None:
        """Тест чтения пустого JSON-файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            tmp_file.write('')
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_json(tmp_file_path)
            assert result == []
        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_invalid_json_file(self) -> None:
        """Тест чтения невалидного JSON-файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            tmp_file.write('{"invalid": "json"')
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_json(tmp_file_path)
            assert result == []
        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_not_list_json(self) -> None:
        """Тест чтения JSON-файла с не-списком."""
        test_data = {"key": "value"}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            json.dump(test_data, tmp_file)
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_json(tmp_file_path)
            assert result == []
        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_file_not_found(self) -> None:
        """Тест чтения несуществующего файла."""
        result = get_transactions_from_json("nonexistent_file.json")
        assert result == []