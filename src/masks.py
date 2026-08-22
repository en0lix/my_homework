from typing import Optional


def get_mask_card_number(card_number: Optional[str]) -> str:
    """Маскирует номер карты"""
    if not card_number:
        return ""

    # Удаляем пробелы и дефисы
    cleaned = ''.join(c for c in str(card_number) if c.isdigit())

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

    cleaned = ''.join(c for c in str(account_number) if c.isdigit())

    if len(cleaned) < 4:
        return str(account_number)

    return f"**{cleaned[-4:]}"