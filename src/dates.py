"""
Модуль dates содержит функции для работы с датами.
"""

from datetime import datetime
from typing import Optional

# Константы
DATE_FORMATS = [
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%d.%m.%Y",
    "%d-%m-%Y",
]


def get_date(date_input: Optional[str]) -> str:
    """
    Парсит дату из различных форматов и возвращает в формате YYYY-MM-DD.

    Args:
        date_input: Строка с датой

    Returns:
        str: Дата в формате YYYY-MM-DD

    Raises:
        ValueError: Если не удалось распарсить дату
    """
    if date_input is None or date_input == "":
        return ""

    date_str = str(date_input).strip()
    if not date_str:
        return ""

    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date: {date_input!r}")
