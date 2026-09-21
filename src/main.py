"""
Точка входа в приложение для анализа транзакций.
"""

import json
import logging
from datetime import datetime

from src.external_api import get_currency_rates, get_stock_prices
from src.utils import read_operations_excel
from src.views import get_main_page_view

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def load_user_settings(path: str = "user_settings.json") -> dict:
    """Загружает настройки пользователя из JSON-файла."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Файл настроек не найден: {path}")
        return {"user_currencies": [], "user_stocks": []}
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка чтения JSON: {e}")
        return {"user_currencies": [], "user_stocks": []}


def main():
    """Запускает приложение и выводит JSON-ответ для главной страницы."""
    logger.info("Приложение запущено")

    # 1. Настройки
    settings = load_user_settings()
    logger.info(f"Настройки загружены: {settings}")

    # 2. Транзакции
    transactions = read_operations_excel("data/operations.xlsx")
    logger.info(f"Загружено {len(transactions)} транзакций")

    # 3. Курсы валют
    rates = get_currency_rates(settings.get("user_currencies", []))
    logger.info(f"Курсы валют: {rates}")

    # 4. Цены акций
    stocks = get_stock_prices(settings.get("user_stocks", []))
    logger.info(f"Цены акций: {stocks}")

    # 5. Дата для фильтра — берём максимальную дату из данных
    if transactions:
        max_date = max(
            tx["Дата операции"] for tx in transactions if tx.get("Дата операции")
        )
        date_str = max_date.strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Используем дату из данных: {date_str}")
    else:
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Используем текущую дату: {date_str}")

    # 6. Формируем JSON-ответ
    result = get_main_page_view(date_str, transactions, rates, stocks)

    # 7. Выводим
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()