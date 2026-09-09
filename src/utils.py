"""
Модуль utils содержит утилиты для работы с данными из различных форматов.
"""

import csv
import json
import logging
import os
from typing import Any, Dict, List, Optional

import pandas as pd

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создание обработчика для записи в файл
file_handler = logging.FileHandler('logs/utils.log', mode='w', encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Создание обработчика для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Формат логов
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавление обработчиков к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл с данными о финансовых транзакциях и возвращает список словарей.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
        Возвращает пустой список, если:
        - Файл не найден
        - Файл пустой
        - Содержимое файла не является списком
    """
    logger.info(f"Начало чтения JSON-файла: {file_path}")

    try:
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            logger.warning(f"Данные не являются списком. Тип: {type(data)}")
            return []

        logger.info(f"Успешно прочитано {len(data)} транзакций из JSON")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return []


def get_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает CSV-файл с данными о финансовых транзакциях и возвращает список словарей.

    Args:
        file_path: Путь к CSV-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
        Возвращает пустой список, если:
        - Файл не найден
        - Файл пустой
        - Произошла ошибка при чтении

    Пример:
        >>> transactions = get_transactions_from_csv("data/transactions.csv")
        >>> print(len(transactions))
        10
    """
    logger.info(f"Начало чтения CSV-файла: {file_path}")

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        # Читаем CSV файл с помощью pandas
        df = pd.read_csv(file_path)

        # Проверяем, что файл не пустой
        if df.empty:
            logger.warning(f"CSV-файл пуст: {file_path}")
            return []

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict('records')

        # Обработка NaN значений (замена на None)
        for transaction in transactions:
            for key, value in transaction.items():
                if pd.isna(value):
                    transaction[key] = None

        logger.info(f"Успешно прочитано {len(transactions)} транзакций из CSV")
        return transactions

    except pd.errors.EmptyDataError:
        logger.warning(f"CSV-файл пуст: {file_path}")
        return []
    except pd.errors.ParserError as e:
        logger.error(f"Ошибка парсинга CSV: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении CSV: {e}")
        return []


def get_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel-файл (XLSX) с данными о финансовых транзакциях и возвращает список словарей.

    Args:
        file_path: Путь к Excel-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
        Возвращает пустой список, если:
        - Файл не найден
        - Файл пустой
        - Произошла ошибка при чтении

    Пример:
        >>> transactions = get_transactions_from_excel("data/transactions_excel.xlsx")
        >>> print(len(transactions))
        10
    """
    logger.info(f"Начало чтения Excel-файла: {file_path}")

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        # Читаем Excel файл с помощью pandas
        df = pd.read_excel(file_path)

        # Проверяем, что файл не пустой
        if df.empty:
            logger.warning(f"Excel-файл пуст: {file_path}")
            return []

        # Преобразуем DataFrame в список словарей
        transactions = df.to_dict('records')

        # Обработка NaN значений (замена на None)
        for transaction in transactions:
            for key, value in transaction.items():
                if pd.isna(value):
                    transaction[key] = None

        logger.info(f"Успешно прочитано {len(transactions)} транзакций из Excel")
        return transactions

    except pd.errors.EmptyDataError:
        logger.warning(f"Excel-файл пуст: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка при чтении Excel: {e}")
        return []


def get_transactions_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Универсальная функция для чтения транзакций из файла.
    Автоматически определяет формат по расширению.

    Args:
        file_path: Путь к файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
        Возвращает пустой список, если:
        - Файл не найден
        - Формат не поддерживается
        - Произошла ошибка при чтении

    Пример:
        >>> transactions = get_transactions_from_file("data/operations.json")
        >>> transactions = get_transactions_from_file("data/transactions.csv")
        >>> transactions = get_transactions_from_file("data/transactions_excel.xlsx")
    """
    logger.info(f"Чтение файла: {file_path}")

    # Проверяем существование файла
    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден: {file_path}")
        return []

    # Определяем расширение файла
    extension = os.path.splitext(file_path)[1].lower()

    # Выбираем функцию для чтения в зависимости от расширения
    if extension == '.json':
        return get_transactions_from_json(file_path)
    elif extension == '.csv':
        return get_transactions_from_csv(file_path)
    elif extension in ['.xlsx', '.xls']:
        return get_transactions_from_excel(file_path)
    else:
        logger.error(f"Неподдерживаемый формат файла: {extension}")
        return []