"""
Тесты для модуля external_api.
"""

from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_currency_to_rub, get_exchange_rate


class TestGetExchangeRate:
    """Тесты для функции get_exchange_rate."""

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_success(self, mock_get: MagicMock) -> None:
        """Тест успешного получения курса валют."""
        # Настраиваем мок ответа
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 85.5}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызываем функцию
        result = get_exchange_rate("USD", "RUB")

        # Проверяем результат
        assert result == 85.5
        mock_get.assert_called_once()

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_api_error(self, mock_get: MagicMock) -> None:
        """Тест ошибки API."""
        # Настраиваем мок с ошибкой
        mock_get.side_effect = Exception("API Error")

        # Вызываем функцию
        result = get_exchange_rate("USD", "RUB")

        # Проверяем результат
        assert result is None

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_no_success(self, mock_get: MagicMock) -> None:
        """Тест ответа API без успеха."""
        # Настраиваем мок с ошибкой
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": False,
            "error": {"info": "Invalid API key"}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызываем функцию
        result = get_exchange_rate("USD", "RUB")

        # Проверяем результат
        assert result is None

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_missing_rate(self, mock_get: MagicMock) -> None:
        """Тест отсутствия курса в ответе."""
        # Настраиваем мок без курса
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызываем функцию
        result = get_exchange_rate("USD", "RUB")

        # Проверяем результат
        assert result is None

    def test_get_exchange_rate_no_api_key(self) -> None:
        """Тест без API ключа."""
        with patch('src.external_api.API_KEY', ''):
            result = get_exchange_rate("USD", "RUB")
            assert result is None


class TestConvertCurrencyToRub:
    """Тесты для функции convert_currency_to_rub."""

    @patch('src.external_api.get_exchange_rate')
    def test_convert_usd_to_rub(self, mock_get_rate: MagicMock) -> None:
        """Тест конвертации USD в рубли."""
        # Настраиваем мок курса
        mock_get_rate.return_value = 85.0

        # Создаем транзакцию
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }

        # Вызываем функцию
        result = convert_currency_to_rub(transaction)

        # Проверяем результат
        assert result == 8500.0
        mock_get_rate.assert_called_once_with("USD", "RUB")

    @patch('src.external_api.get_exchange_rate')
    def test_convert_eur_to_rub(self, mock_get_rate: MagicMock) -> None:
        """Тест конвертации EUR в рубли."""
        # Настраиваем мок курса
        mock_get_rate.return_value = 90.0

        # Создаем транзакцию
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "EUR"}
            }
        }

        # Вызываем функцию
        result = convert_currency_to_rub(transaction)

        # Проверяем результат
        assert result == 9000.0
        mock_get_rate.assert_called_once_with("EUR", "RUB")

    @patch('src.external_api.get_exchange_rate')
    def test_convert_currency_rate_failure(self, mock_get_rate: MagicMock) -> None:
        """Тест при неудачном получении курса."""
        # Настраиваем мок с ошибкой
        mock_get_rate.return_value = None

        # Создаем транзакцию
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        }

        # Вызываем функцию
        result = convert_currency_to_rub(transaction)

        # Проверяем результат (возвращает исходную сумму)
        assert result == 100.0

    def test_convert_rub_to_rub(self) -> None:
        """Тест конвертации рублей в рубли (без изменений)."""
        # Создаем транзакцию
        transaction = {
            "operationAmount": {
                "amount": "1000",
                "currency": {"code": "RUB"}
            }
        }

        # Вызываем функцию
        result = convert_currency_to_rub(transaction)

        # Проверяем результат
        assert result == 1000.0

    def test_convert_missing_amount(self) -> None:
        """Тест с отсутствующей суммой."""
        # Создаем транзакцию без суммы
        transaction = {
            "operationAmount": {
                "currency": {"code": "USD"}
            }
        }

        # Вызываем функцию
        result = convert_currency_to_rub(transaction)

        # Проверяем результат
        assert result == 0.0

    def test_convert_invalid_amount(self) -> None:
        """Тест с невалидной суммой."""
        # Создаем транзакцию с невалидной суммой
        transaction = {
            "operationAmount": {
                "amount": "invalid",
                "currency": {"code": "USD"}
            }
        }

        # Вызываем функцию
        result = convert_currency_to_rub(transaction)

        # Проверяем результат
        assert result == 0.0

    def test_convert_missing_currency(self) -> None:
        """Тест с отсутствующей валютой."""
        # Создаем транзакцию без валюты
        transaction = {
            "operationAmount": {
                "amount": "100"
            }
        }

        # Вызываем функцию
        result = convert_currency_to_rub(transaction)

        # Проверяем результат (по умолчанию RUB)
        assert result == 100.0