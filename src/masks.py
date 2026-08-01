def get_mask_account(account: int | str) -> str:
    """Функция маскировки банковского счета"""
    account = str(account)
    if len(account) < 4:
        raise ValueError("Неправильно")
    mask = "**"
    part = account[-4:]
    return mask + part


def get_mask_card_number(card_number: int | str) -> str:
    """Функция маскировки номера карты"""
    card_number = str(card_number)
    if len(card_number) != 16:
        raise ValueError("Неправильно")
    block_1 = card_number[:4]
    block_2 = card_number[4:6] + "**"
    block_3 = "****"
    block_4 = card_number[12:]
    return block_1 + " " + block_2 + " " + block_3 + " " + block_4


if __name__ == "__main__":
    account = 7365410843013587
    print(get_mask_card_number(account))

from typing import Optional


def get_mask_card_number(card: Optional[str]) -> str:
    """
    Маска карты: первые 6 + ***** + последние 4.
    Вход может содержать пробелы/тире.
    """
    if card is None or card == "":
        return ""

    digits = "".join(ch for ch in str(card) if ch.isdigit())

    # Карта: 13–19 цифр
    if 13 <= len(digits) <= 19:
        masked = digits[:6] + "*" * (len(digits) - 10) + digits[-4:]
        return masked

    raise ValueError("Invalid card number")


def get_mask_account(account: Optional[str]) -> str:
    """
    Маска счёта: ***** + последние 4 цифры.
    Требуется минимум 4 цифры.
    """
    if account is None or account == "":
        return ""

    digits = "".join(ch for ch in str(account) if ch.isdigit())

    if len(digits) >= 4:
        masked = "*" * (len(digits) - 4) + digits[-4:]
        return masked

    raise ValueError("Invalid account number")


from typing import Optional


def get_mask_card_number(card: Optional[str]) -> str:
    if card is None or card == "":
        return ""
    digits = "".join(ch for ch in str(card) if ch.isdigit())
    if len(digits) < 13 or len(digits) > 19:
        raise ValueError("Invalid card number length")
    return digits[:6] + "*" * (len(digits) - 10) + digits[-4:]


def get_mask_account(account: Optional[str]) -> str:
    if account is None or account == "":
        return ""
    digits = "".join(ch for ch in str(account) if ch.isdigit())
    if len(digits) < 4:
        raise ValueError("Invalid account number length")
    return "*" * (len(digits) - 4) + digits[-4:]


def mask_account_card(value: Optional[str]) -> str:
    if value is None or value == "":
        return ""
    digits = "".join(ch for ch in str(value) if ch.isdigit())

    # Карта: 13–19 цифр
    if 13 <= len(digits) <= 19:
        return digits[:6] + "*" * (len(digits) - 10) + digits[-4:]

    # Счёт: >= 4 цифр и не карта
    if len(digits) >= 4:
        return "*" * (len(digits) - 4) + digits[-4:]

    raise ValueError("Invalid input: not a card and not a valid account")
