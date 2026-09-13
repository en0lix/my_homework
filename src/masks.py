from typing import Optional


def get_mask_card_number(card_number: Optional[str]) -> str:
    """Маскирует номер карты"""
    if not card_number:
        return ""

    # Удаляем пробелы и дефисы
    cleaned = "".join(c for c in str(card_number) if c.isdigit())

    if len(cleaned) < 4:
        return str(card_number)

    if len(cleaned) >= 16:
        # Маскируем: первые 6 цифр, затем 4 звезды, последние 4 цифры
        return f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}"
    elif len(cleaned) >= 14:
        return f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}"
    else:
        return str(card_number)


def get_mask_account(account_number: Optional[str]) -> str:
    """Маскирует номер счета"""
    if not account_number:
        return ""

    cleaned = "".join(c for c in str(account_number) if c.isdigit())

    if len(cleaned) < 4:
        return str(account_number)

    return f"**{cleaned[-4:]}"


"""
Модуль masks содержит функции для маскирования банковских карт и счетов.
"""

import logging
import re
from typing import Optional

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создание обработчика для записи в файл
file_handler = logging.FileHandler('logs/masks.log', mode='w', encoding='utf-8')
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


def get_mask_card_number(card_number: Optional[str]) -> str:
    """
    Маскирует номер банковской карты.

    Args:
        card_number: Номер карты (может содержать пробелы, дефисы)

    Returns:
        str: Замаскированный номер карты в формате XXXX XX** **** XXXX

    Пример:
        >>> get_mask_card_number("1234567890123456")
        "1234 56** **** 3456"
    """
    logger.info(f"Маскирование номера карты: {card_number}")

    if card_number is None or card_number == "":
        logger.warning("Пустой номер карты")
        return ""

    # Удаляем все нецифровые символы
    cleaned = re.sub(r'\D', '', str(card_number))

    if len(cleaned) < 4:
        logger.warning(f"Номер карты слишком короткий: {cleaned}")
        return str(card_number)

    if len(cleaned) >= 16:
        # Маскируем: первые 6 цифр, затем 4 звезды, последние 4 цифры
        masked = f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}"
        logger.info(f"Номер карты замаскирован: {masked}")
        return masked
    else:
        # Для коротких номеров возвращаем как есть
        logger.warning(f"Нестандартная длина номера карты: {len(cleaned)}")
        return str(card_number)


def get_mask_account(account_number: Optional[str]) -> str:
    """
    Маскирует номер банковского счета.

    Args:
        account_number: Номер счета

    Returns:
        str: Замаскированный номер счета в формате **XXXX

    Пример:
        >>> get_mask_account("12345678901234567890")
        "**7890"
    """
    logger.info(f"Маскирование номера счета: {account_number}")

    if account_number is None or account_number == "":
        logger.warning("Пустой номер счета")
        return ""

    # Удаляем все нецифровые символы
    cleaned = re.sub(r'\D', '', str(account_number))

    if len(cleaned) < 4:
        logger.warning(f"Номер счета слишком короткий: {cleaned}")
        return str(account_number)

    # Показываем только последние 4 цифры
    masked = f"**{cleaned[-4:]}"
    logger.info(f"Номер счета замаскирован: {masked}")
    return masked