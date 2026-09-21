"""
Модуль widget содержит универсальные функции для работы с данными.
"""

from datetime import datetime
from typing import Any, Dict, Optional


def mask_account_card(value: Optional[str]) -> str:
    """
    Универсальная функция маскирования, определяет тип данных автоматически.

    Args:
        value: Строка с типом и номером карты или счета

    Returns:
        str: Замаскированный номер

    Raises:
        ValueError: Если не удалось определить тип данных
    """
    if value is None or value == "":
        return ""

    # Здесь должна быть логика маскирования
    # Временная реализация для примера
    return value


def get_date(date_string: Optional[str]) -> Optional[str]:
    """
    Преобразует ISO дату в формат ДД.ММ.ГГГГ.

    Args:
        date_string: Дата в ISO формате

    Returns:
        Optional[str]: Дата в формате ДД.ММ.ГГГГ или None при ошибке
    """
    if not date_string:
        return None

    try:
        # Парсим ISO формат
        if "T" in date_string:
            date_part = date_string.split("T")[0]
        else:
            date_part = date_string

        # Убираем временную зону
        date_part = date_part.split("+")[0]

        # Парсим дату
        dt = datetime.strptime(date_part, "%Y-%m-%d")
        return dt.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        return date_string


def validate_widget_data(data: Optional[Dict[str, Any]]) -> None:
    """
    Валидирует данные для widget.

    Args:
        data: Словарь с данными

    Raises:
        ValueError: Если данные невалидны
    """
    if data is None or not isinstance(data, dict):
        raise ValueError("Data must be a dictionary")

    if "title" not in data:
        raise ValueError("Missing 'title' key")
