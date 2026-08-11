# src/generators.py  (или generators.py, если без src)
def filter_by_currency(transactions, currency):
    """Возвращает транзакции только указанной валюты."""
    return [t for t in transactions if t.get("currency") == currency]

def filter_by_currency(transactions, currency):
    """
    Возвращает список транзакций, где валюта совпадает с указанной.

    :param transactions: список словарей с транзакциями, каждый содержит ключ 'currency'
    :param currency: строка с кодом валюты (например, 'RUB', 'USD')
    :return: список подходящих транзакций
    """
    return [t for t in transactions if t.get("currency") == currency]
