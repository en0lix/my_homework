"""
Модуль main содержит основную логику программы работы с банковскими транзакциями.
"""

import logging
from typing import Any, Dict, List

from src.processing import filter_by_state, sort_by_date
from src.utils import (
    get_transactions_from_csv,
    get_transactions_from_excel,
    get_transactions_from_json,
    process_bank_search,
)
from src.widget import get_date, mask_account_card

logger = logging.getLogger(__name__)

AVAILABLE_STATUSES = ("EXECUTED", "CANCELED", "PENDING")


def ask_menu_choice() -> str:
    """Спрашивает у пользователя выбор формата файла (1, 2 или 3)."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        choice = input("Ваш выбор: ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print("Некорректный выбор. Попробуйте снова.")


def read_transactions(choice: str) -> List[Dict[str, Any]]:
    """Читает транзакции в зависимости от выбора пользователя."""
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        return get_transactions_from_json("data/operations.json")
    if choice == "2":
        print("Для обработки выбран CSV-файл.")
        return get_transactions_from_csv("data/transactions.csv")
    if choice == "3":
        print("Для обработки выбран XLSX-файл.")
        return get_transactions_from_excel("data/transactions_excel.xlsx")
    return []


def ask_status() -> str:
    """Спрашивает статус фильтрации, повторяет запрос при ошибке."""
    while True:
        print(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            f"Доступные для фильтровки статусы: {', '.join(AVAILABLE_STATUSES)}"
        )
        status = input("Статус: ").strip().upper()

        if status in AVAILABLE_STATUSES:
            print(f'Операции отфильтрованы по статусу "{status}"')
            return status

        print(f'Статус операции "{status}" недоступен.')


def ask_yes_no(question: str) -> bool:
    """Задаёт вопрос с ответом Да/Нет и возвращает булево значение."""
    while True:
        answer = input(f"{question} Да/Нет: ").strip().lower()
        if answer in ("да", "yes", "y", "д"):
            return True
        if answer in ("нет", "no", "n", "н"):
            return False
        print("Пожалуйста, ответьте 'Да' или 'Нет'.")


def ask_sort_direction() -> bool:
    """Спрашивает направление сортировки (возвращает reverse)."""
    while True:
        answer = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        if "возр" in answer:
            return False
        if "убыв" in answer:
            return True
        print("Введите 'по возрастанию' или 'по убыванию'.")


def is_ruble_transaction(transaction: Dict[str, Any]) -> bool:
    """Проверяет, что транзакция в рублях."""
    code = (
        transaction.get("operationAmount", {})
        .get("currency", {})
        .get("code", "")
    )
    return code == "RUB"


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода в консоль."""
    date_raw = transaction.get("date", "")
    date = get_date(date_raw) or date_raw
    description = transaction.get("description", "") or ""
    from_acc = transaction.get("from") or ""
    to_acc = transaction.get("to") or ""

    from_masked = mask_account_card(from_acc) if from_acc else ""
    to_masked = mask_account_card(to_acc) if to_acc else ""

    amount = transaction.get("operationAmount", {}).get("amount", "0")
    code = (
        transaction.get("operationAmount", {})
        .get("currency", {})
        .get("code", "")
    )
    symbol = "руб." if code == "RUB" else code

    lines = [f"{date} {description}".strip()]
    if from_masked and to_masked:
        lines.append(f"{from_masked} -> {to_masked}")
    elif to_masked:
        lines.append(to_masked)
    lines.append(f"Сумма: {amount} {symbol}".strip())
    return "\n".join(lines)


def main() -> None:
    """Основная логика программы работы с банковскими транзакциями."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # 1. Выбор файла
    choice = ask_menu_choice()
    transactions = read_transactions(choice)

    if not transactions:
        print("Не удалось загрузить транзакции из файла.")
        return

    # 2. Фильтр по статусу
    status = ask_status()
    transactions = filter_by_state(transactions, status)

    # 3. Сортировка по дате
    if ask_yes_no("Отсортировать операции по дате?"):
        reverse = ask_sort_direction()
        transactions = sort_by_date(transactions, reverse=reverse)

    # 4. Только рублёвые транзакции
    if ask_yes_no("Выводить только рублевые транзакции?"):
        transactions = [t for t in transactions if is_ruble_transaction(t)]

    # 5. Поиск по слову в описании
    if ask_yes_no(
        "Отфильтровать список транзакций по определенному слову в описании?"
    ):
        search = input("Введите слово для поиска: ").strip()
        transactions = process_bank_search(transactions, search)

    # 6. Вывод
    print("\nРаспечатываю итоговый список транзакций...\n")

    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")
    for transaction in transactions:
        print(format_transaction(transaction))
        print()


if __name__ == "__main__":
    main()