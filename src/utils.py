"""
Модуль utils содержит утилиты для работы с данными.
"""

import json
import os
from typing import Any, Dict, List


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
    try:
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, FileNotFoundError, ValueError):
        return []


"""
Модуль utils содержит утилиты для работы с данными.
"""

import json
import logging
import os
from typing import Any, Dict, List

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
    logger.info(f"Начало чтения файла: {file_path}")

    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        logger.info(f"Файл найден: {file_path}")

        # Читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        logger.info(f"Файл успешно прочитан. Тип данных: {type(data)}")

        # Проверяем, что данные являются списком
        if not isinstance(data, list):
            logger.warning(f"Данные не являются списком. Тип: {type(data)}")
            return []

        logger.info(f"Получено {len(data)} транзакций")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON: {e}")
        return []
    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
        return []
    except ValueError as e:
        logger.error(f"Ошибка значения: {e}")
        return []
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return []
