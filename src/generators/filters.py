def filter_by_currency(transactions, currency_code):
    """
    Генератор: возвращает транзакции, где currency.code == currency_code.

    :param transactions: список словарей транзакций
    :param currency_code: код валюты, например "USD"
    :return: итератор по подходящим транзакциям
    """
    for transaction in transactions:
        amount = transaction.get("operationAmount", {})
        currency = amount.get("currency", {})
        if currency.get("code") == currency_code:
            yield transaction


from generators import filter_by_currency

transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 123456789,
        "state": "EXECUTED",
        "date": "2019-01-01T10:00:00.000000",
        "operationAmount": {"amount": "5000.00", "currency": {"name": "RUB", "code": "RUB"}},
        "description": "Перевод в рублях",
        "from": "Счет 00001111222233334444",
        "to": "Счет 55556666777788889999",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
]

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))


def transaction_descriptions(transactions):
    """
    Генератор, который принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди.

    Предполагается, что в словаре есть ключ 'type', определяющий тип транзакции.
    """
    type_to_description = {
        "org_transfer": "Перевод организации",
        "account_to_account": "Перевод со счета на счет",
        "card_to_card": "Перевод с карты на карту",
        # добавь сюда другие типы, если нужны
    }

    for txn in transactions:
        txn_type = txn.get("type")
        # Если тип известен — берём из словаря, иначе возвращаем заглушку
        yield type_to_description.get(txn_type, f"Неизвестная операция ({txn_type})")


# Пример использования
if __name__ == "__main__":
    transactions = [
        {"type": "org_transfer"},
        {"type": "account_to_account"},
        {"type": "account_to_account"},
        {"type": "card_to_card"},
        {"type": "org_transfer"},
        {"type": "unknown_type"},  # для проверки обработки неизвестного типа
    ]

    descriptions = transaction_descriptions(transactions)
    for _ in range(5):
        print(next(descriptions))

    def card_number_generator(start: int, end: int):
        """
        Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

        Диапазон: от 0000 0000 0000 0001 до 9999 9999 9999 9999.
        Принимает start и end как целые числа (без пробелов и разделителей).

        Пример:
            for card_number in card_number_generator(1, 5):
                print(card_number)
        >>> 0000 0000 0000 0001
            0000 0000 0000 0002
            ...
        """
        if start < 1 or end > 9999_9999_9999_9999:
            raise ValueError("Диапазон должен быть от 1 до 9999999999999999")
        if start > end:
            return  # пустой генератор, если начало больше конца

        for number in range(start, end + 1):
            # Форматируем число как 16 цифр с ведущими нулями
            s = f"{number:016d}"
            # Разбиваем на группы по 4 цифры через пробел
            yield f"{s[0:4]} {s[4:8]} {s[8:12]} {s[12:16]}"
