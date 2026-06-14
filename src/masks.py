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
