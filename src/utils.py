"""
Модуль utils содержит утилиты для чтения данных.
"""

import logging
import os
from typing import Any, Dict, List

import pandas as pd

logger = logging.getLogger(__name__)


def read_operations_excel(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает Excel-файл с транзакциями. Поддерживает два формата:
    1. Банковская выписка (Дата операции, Номер карты, Сумма платежа, ...)
    2. Экспорт JSON (id, state, date, amount, currency_code, from, to, description)
    """
    if not os.path.exists(file_path):
        logger.warning(f"Файл не найден: {file_path}")
        return []

    try:
        df = pd.read_excel(file_path)
        logger.info(f"Колонки в файле: {df.columns.tolist()}")

        # ===== Определяем формат =====
        is_bank_format = "Дата операции" in df.columns
        is_json_export = "date" in df.columns and "amount" in df.columns

        if is_bank_format:
            # Банковская выписка
            df["Дата операции"] = pd.to_datetime(df["Дата операции"], errors="coerce")
            if "Сумма платежа" in df.columns:
                df["Сумма платежа"] = pd.to_numeric(
                    df["Сумма платежа"].astype(str).str.replace(",", ".").str.replace(" ", ""),
                    errors="coerce",
                )
            else:
                df["Сумма платежа"] = pd.to_numeric(df.get("Сумма операции", 0), errors="coerce")
            df["Кэшбэк"] = (
                pd.to_numeric(
                    df["Кэшбэк"].astype(str).str.replace(",", ".").str.replace(" ", ""),
                    errors="coerce",
                ).fillna(0)
                if "Кэшбэк" in df.columns
                else 0
            )

        elif is_json_export:
            # JSON-экспорт
            df = df.rename(
                columns={
                    "date": "Дата операции",
                    "amount": "Сумма платежа",
                    "description": "Описание",
                    "state": "Статус",
                    "from": "Откуда",
                    "to": "Куда",
                    "currency_code": "Валюта операции",
                }
            )
            df["Дата операции"] = pd.to_datetime(
                df["Дата операции"], errors="coerce", utc=True
            ).dt.tz_localize(None)
            df["Сумма платежа"] = pd.to_numeric(df["Сумма платежа"], errors="coerce")
            df["Кэшбэк"] = 0
            df["Категория"] = ""
            df["Номер карты"] = ""

        else:
            logger.error(f"Неизвестный формат файла. Колонки: {df.columns.tolist()}")
            return []

        # Заполняем пустые значения
        for col in [
            "Номер карты",
            "Категория",
            "Описание",
            "Статус",
            "Откуда",
            "Куда",
            "Валюта операции",
        ]:
            if col in df.columns:
                df[col] = df[col].fillna("").astype(str)
            else:
                df[col] = ""

        df = df.dropna(subset=["Дата операции", "Сумма платежа"])
        logger.info(f"Успешно загружено {len(df)} транзакций")
        return df.to_dict("records")

    except Exception as e:
        logger.error(f"Ошибка чтения Excel: {e}", exc_info=True)
        return []
