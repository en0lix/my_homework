"""
Модуль masks содержит функции для маскирования банковских карт и счетов.
"""

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


def get_mask_card_number(card_number: Optional[str]) -> str:
    """
    Маскирует номер банковской карты.
    """
    if card_number is None or card_number == "":
        return ""

    cleaned = re.sub(r"\D", "", str(card_number))

    if len(cleaned) < 4:
        return str(card_number)

    if len(cleaned) >= 16:
        return f"{cleaned[:4]} {cleaned[4:6]}** **** {cleaned[-4:]}"
    return str(card_number)


def get_mask_account(account_number: Optional[str]) -> str:
    """
    Маскирует номер банковского счета.
    """
    if account_number is None or account_number == "":
        return ""

    cleaned = re.sub(r"\D", "", str(account_number))

    if len(cleaned) < 4:
        return str(account_number)

    return f"**{cleaned[-4:]}"
