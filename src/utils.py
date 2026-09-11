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

"""
Модуль utils содержит утилиты для работы с данными.
"""

import json
import logging
import os
import re
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


def get_transactions_from_json(file_path: str) -> List[Dict[str, Any]]:
    """Читает JSON-файл с транзакциями."""
    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден: {file_path}")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except (json.JSONDecodeError, OSError) as e:
        logger.error(f"Ошибка чтения JSON: {e}")
        return []


def get_transactions_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Читает CSV-файл с транзакциями."""
    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден: {file_path}")
        return []
    try:
        df = pd.read_csv(file_path)
        return df.to_dict("records") if not df.empty else []
    except Exception as e:
        logger.error(f"Ошибка чтения CSV: {e}")
        return []


def get_transactions_from_excel(file_path: str) -> List[Dict[str, Any]]:
    """Читает Excel-файл с транзакциями."""
    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден: {file_path}")
        return []
    try:
        df = pd.read_excel(file_path)
        return df.to_dict("records") if not df.empty else []
    except Exception as e:
        logger.error(f"Ошибка чтения Excel: {e}")
        return []


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """
    Фильтрует транзакции по строке поиска в описании с использованием регулярных выражений.

    Args:
        data: Список словарей с данными о банковских операциях
        search: Строка поиска

    Returns:
        List[Dict[str, Any]]: Список транзакций, в описании которых найдена строка поиска

    Пример:
        >>> data = [{"description": "Перевод организации"}, {"description": "Открытие вклада"}]
        >>> process_bank_search(data, "Перевод")
        [{"description": "Перевод организации"}]
    """
    if not data or not search:
        return []

    try:
        # Экранируем спецсимволы и компилируем regex без учёта регистра
        pattern = re.compile(re.escape(search), re.IGNORECASE)
    except re.error as e:
        logger.error(f"Ошибка компиляции regex: {e}")
        return []

    result = []
    for transaction in data:
        description = transaction.get("description", "") or ""
        if pattern.search(str(description)):
            result.append(transaction)
    return result


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Считает количество операций по каждой категории из списка.

    Args:
        data: Список словарей с данными о банковских операциях
        categories: Список категорий операций (по полю description)

    Returns:
        Dict[str, int]: Словарь {категория: количество операций}

    Пример:
        >>> data = [{"description": "Перевод организации"}, {"description": "Перевод организации"}]
        >>> process_bank_operations(data, ["Перевод организации"])
        {"Перевод организации": 2}
    """
    result: Dict[str, int] = {category: 0 for category in categories}

    if not data or not categories:
        return result

    # Компилируем шаблоны для каждой категории
    patterns = {
        category: re.compile(re.escape(category), re.IGNORECASE)
        for category in categories
    }

    for transaction in data:
        description = str(transaction.get("description", "") or "")
        for category, pattern in patterns.items():
            if pattern.search(description):
                result[category] += 1
                # Если описание подходит под одну категорию — не считаем её в других
                break

    return result