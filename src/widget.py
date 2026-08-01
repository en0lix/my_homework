import re
from datetime import datetime


def get_date(date: str) -> str:
    """Функция преобразует дату в формат 'DD.MM.YYYY'"""
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    return date.strftime("%d.%m.%Y")


def get_mask_account_card(account_card: str) -> str:
    """
    Принимает один аргумент — строку, содержащую тип и номер карты или счета,
     и возвращает строку с замаскированным номером.
    """
    if "Счет" in account_card:
        letters_count = "".join(re.findall(r"\D+", account_card))
        numbers_count = "".join(re.findall(r"\d+", account_card))
        return f"{letters_count} {get_mask_account(numbers_count)}"
    else:
        letters_card = "".join(re.findall(r"\D+", account_card))
        numbers_card = "".join(re.findall(r"\d+", account_card))
        return f"{letters_card} {get_mask_card_number(numbers_card)}"


from typing import Optional

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(value: Optional[str]) -> str:
    """
    Универсальная маска: если похоже на карту (13–19 цифр) — маска карты,
    иначе если >= 4 цифр — маска счёта, иначе ValueError.
    None/пустая строка → "".
    """
    if value is None or value == "":
        return ""

    digits = "".join(ch for ch in str(value) if ch.isdigit())

    if 13 <= len(digits) <= 19:
        return get_mask_card_number(value)

    if len(digits) >= 4:
        return get_mask_account(value)

    raise ValueError("Cannot determine mask type: not a valid card or account")
