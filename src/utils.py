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
