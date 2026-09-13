# test_functions.py
from src.utils import get_transactions_from_csv, get_transactions_from_excel, get_transactions_from_file

# Проверка чтения CSV
csv_transactions = get_transactions_from_csv("data/transactions.csv")
print(f"CSV транзакций: {len(csv_transactions)}")

# Проверка чтения Excel
excel_transactions = get_transactions_from_excel("data/transactions_excel.xlsx")
print(f"Excel транзакций: {len(excel_transactions)}")

# Проверка универсальной функции
json_transactions = get_transactions_from_file("data/operations.json")
csv_transactions = get_transactions_from_file("data/transactions.csv")
excel_transactions = get_transactions_from_file("data/transactions_excel.xlsx")

print(f"JSON: {len(json_transactions)} транзакций")
print(f"CSV: {len(csv_transactions)} транзакций")
print(f"Excel: {len(excel_transactions)} транзакций")