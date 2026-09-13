"""
Тесты для чтения CSV и Excel файлов.
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.utils import (
    get_transactions_from_csv,
    get_transactions_from_excel,
    get_transactions_from_file,
)


class TestGetTransactionsFromCsv:
    """Тесты для функции get_transactions_from_csv."""

    def test_valid_csv_file(self) -> None:
        """Тест чтения валидного CSV-файла."""
        # Создаем тестовый CSV файл
        test_data = pd.DataFrame([
            {"id": 1, "state": "EXECUTED", "amount": 100},
            {"id": 2, "state": "PENDING", "amount": 200},
        ])

        with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.csv',
                delete=False,
                newline='',
                encoding='utf-8'
        ) as tmp_file:
            test_data.to_csv(tmp_file.name, index=False)
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_csv(tmp_file_path)

            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[0]["state"] == "EXECUTED"
            assert result[0]["amount"] == 100
            assert result[1]["id"] == 2
            assert result[1]["state"] == "PENDING"
            assert result[1]["amount"] == 200

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_empty_csv_file(self) -> None:
        """Тест чтения пустого CSV-файла."""
        with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.csv',
                delete=False,
                newline='',
                encoding='utf-8'
        ) as tmp_file:
            tmp_file.write('')
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_csv(tmp_file_path)
            assert result == []

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_csv_file_not_found(self) -> None:
        """Тест чтения несуществующего CSV-файла."""
        result = get_transactions_from_csv("nonexistent.csv")
        assert result == []

    def test_csv_with_headers_only(self) -> None:
        """Тест CSV-файла только с заголовками."""
        with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.csv',
                delete=False,
                newline='',
                encoding='utf-8'
        ) as tmp_file:
            tmp_file.write('id,state,amount\n')
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_csv(tmp_file_path)
            assert result == []

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    @patch('src.utils.pd.read_csv')
    def test_csv_parser_error(self, mock_read_csv: MagicMock) -> None:
        """Тест ошибки парсинга CSV."""
        mock_read_csv.side_effect = pd.errors.ParserError("Parse error")

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp_file:
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_csv(tmp_file_path)
            assert result == []

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)


class TestGetTransactionsFromExcel:
    """Тесты для функции get_transactions_from_excel."""

    def test_valid_excel_file(self) -> None:
        """Тест чтения валидного Excel-файла."""
        # Создаем тестовый Excel файл
        test_data = pd.DataFrame([
            {"id": 1, "state": "EXECUTED", "amount": 100},
            {"id": 2, "state": "PENDING", "amount": 200},
        ])

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            test_data.to_excel(tmp_file.name, index=False)
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_excel(tmp_file_path)

            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[0]["state"] == "EXECUTED"
            assert result[0]["amount"] == 100
            assert result[1]["id"] == 2
            assert result[1]["state"] == "PENDING"
            assert result[1]["amount"] == 200

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_empty_excel_file(self) -> None:
        """Тест чтения пустого Excel-файла."""
        # Создаем пустой Excel файл
        test_data = pd.DataFrame()

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            test_data.to_excel(tmp_file.name, index=False)
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_excel(tmp_file_path)
            assert result == []

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_excel_file_not_found(self) -> None:
        """Тест чтения несуществующего Excel-файла."""
        result = get_transactions_from_excel("nonexistent.xlsx")
        assert result == []


class TestGetTransactionsFromFile:
    """Тесты для универсальной функции get_transactions_from_file."""

    def test_read_json_file(self) -> None:
        """Тест чтения JSON-файла."""
        import json

        test_data = [{"id": 1, "state": "EXECUTED"}]

        with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.json',
                delete=False,
                encoding='utf-8'
        ) as tmp_file:
            json.dump(test_data, tmp_file)
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_file(tmp_file_path)
            assert result == test_data

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_read_csv_file(self) -> None:
        """Тест чтения CSV-файла."""
        test_data = pd.DataFrame([{"id": 1, "state": "EXECUTED"}])

        with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.csv',
                delete=False,
                newline='',
                encoding='utf-8'
        ) as tmp_file:
            test_data.to_csv(tmp_file.name, index=False)
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_file(tmp_file_path)

            assert len(result) == 1
            assert result[0]["id"] == 1
            assert result[0]["state"] == "EXECUTED"

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_read_excel_file(self) -> None:
        """Тест чтения Excel-файла."""
        test_data = pd.DataFrame([{"id": 1, "state": "EXECUTED"}])

        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            test_data.to_excel(tmp_file.name, index=False)
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_file(tmp_file_path)

            assert len(result) == 1
            assert result[0]["id"] == 1
            assert result[0]["state"] == "EXECUTED"

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_unsupported_format(self) -> None:
        """Тест с неподдерживаемым форматом файла."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(b'test content')
            tmp_file_path = tmp_file.name

        try:
            result = get_transactions_from_file(tmp_file_path)
            assert result == []

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_file_not_found(self) -> None:
        """Тест с несуществующим файлом."""
        result = get_transactions_from_file("nonexistent.file")
        assert result == []