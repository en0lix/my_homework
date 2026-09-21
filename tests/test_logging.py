"""
Тесты для проверки логирования.
"""

import logging
import os
import tempfile
from unittest.mock import patch

import pytest

from src import masks, utils


class TestMasksLogging:
    """Тесты для проверки логирования в модуле masks."""

    def test_get_mask_card_number_logging(self, caplog) -> None:
        """Тест логирования маскирования карты."""
        with caplog.at_level(logging.INFO):
            masks.get_mask_card_number("1234567890123456")

            assert "Маскирование номера карты: 1234567890123456" in caplog.text
            assert "Номер карты замаскирован: 1234 56** **** 3456" in caplog.text

    def test_get_mask_card_number_empty_logging(self, caplog) -> None:
        """Тест логирования пустого номера карты."""
        with caplog.at_level(logging.WARNING):
            masks.get_mask_card_number("")

            assert "Пустой номер карты" in caplog.text

    def test_get_mask_account_logging(self, caplog) -> None:
        """Тест логирования маскирования счета."""
        with caplog.at_level(logging.INFO):
            masks.get_mask_account("12345678901234567890")

            assert "Маскирование номера счета: 12345678901234567890" in caplog.text
            assert "Номер счета замаскирован: **7890" in caplog.text


class TestUtilsLogging:
    """Тесты для проверки логирования в модуле utils."""

    def test_get_transactions_from_json_logging(self, caplog) -> None:
        """Тест логирования чтения JSON-файла."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            tmp_file.write('[]')
            tmp_file_path = tmp_file.name

        try:
            with caplog.at_level(logging.INFO):
                utils.get_transactions_from_json(tmp_file_path)

                assert "Начало чтения файла:" in caplog.text
                assert "Файл найден:" in caplog.text
                assert "Файл успешно прочитан" in caplog.text
                assert "Получено 0 транзакций" in caplog.text
        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def test_get_transactions_from_json_not_found_logging(self, caplog) -> None:
        """Тест логирования при отсутствии файла."""
        with caplog.at_level(logging.WARNING):
            utils.get_transactions_from_json("nonexistent.json")

            assert "Файл не найден: nonexistent.json" in caplog.text