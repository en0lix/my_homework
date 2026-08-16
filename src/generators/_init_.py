def filter_by_currency(transactions, currency):
    """
    Возвращает список транзакций, где валюта совпадает с указанной.

    :param transactions: список словарей, каждый с ключом 'currency'
    :param currency: строка с валютой, например 'RUB' или 'USD'
    :return: список подходящих транзакций
    """
    return [t for t in transactions if t.get("currency") == currency]
