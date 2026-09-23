PythonProject5 — my_homework-main

Набор утилит для работы с данными: маскирование платёжных реквизитов, валидация и форматирование виджетов, фильтрация и сортировка записей. Проект включает тесты (pytest), проверку покрытия (pytest-cov), статический анализ (flake8, mypy) и автоформатирование (Black, isort).

Цель проекта
Реализовать и протестировать набор функций для обработки пользовательских данных:

Маскирование: get_mask_card_number, get_mask_account, mask_account_card — безопасное скрытие чувствительных данных.
Работа с датами: get_date — парсинг и нормализация дат.
Фильтрация и сортировка: filter_by_state, sort_by_date — выборка и упорядочивание записей.
Виджеты: format_widget, validate_widget_data — валидация и форматирование данных виджетов с обработкой краевых случаев (None, пустые строки, пробелы).
Генераторы и вспомогательные утилиты в модуле processing.
Проект демонстрирует:

корректную валидацию входных данных (выброс ValueError при недопустимых значениях);
покрытие тестами не менее 80%;
соблюдение стандартов кода (Black, isort, flake8, mypy).
Использование функций
1. Модуль processing — Обработка транзакций
filter_by_state(transactions, state="EXECUTED")
Фильтрует транзакции по заданному статусу.

Параметры:

transactions (list[dict]) — список транзакций

state (str) — статус для фильтрации (по умолчанию "EXECUTED")

Возвращает: list[dict] — отфильтрованный список

python
from src.processing import filter_by_state

transactions = [
    {"id": 1, "state": "EXECUTED", "date": "2026-08-22"},
    {"id": 2, "state": "PENDING", "date": "2026-08-21"},
    {"id": 3, "state": "EXECUTED", "date": "2026-08-20"},
    {"id": 4, "state": "CANCELLED", "date": "2026-08-19"},
]

# Фильтрация по статусу EXECUTED
executed = filter_by_state(transactions)
print(executed)

# Фильтрация по статусу PENDING
pending = filter_by_state(transactions, "PENDING"

# Фильтрация по несуществующему статусу
completed = filter_by_state(transactions, "COMPLETED")
print(completed)

sort_by_date(transactions, reverse=True)
Сортирует транзакции по дате.

Параметры:

transactions (list[dict]) — список транзакций

reverse (bool) — True (по умолчанию) — новые сверху, False — старые сверху

Возвращает: list[dict] — отсортированный список

python
from src.processing import sort_by_date

transactions = [
    {"id": 1, "date": "2026-08-22T10:00:00"},
    {"id": 2, "date": "2026-08-21T15:30:00"},
    {"id": 3, "date": "2026-08-20T09:15:00"},
]

# Сортировка по убыванию (новые → старые) — по умолчанию
sorted_desc = sort_by_date(transactions)
print([t["id"] for t in sorted_desc])


# Сортировка по возрастанию (старые → новые)
sorted_asc = sort_by_date(transactions, reverse=False)
print([t["id"] for t in sorted_asc])

2. Модуль masks — Маскирование данных
get_mask_card_number(card_number)
Маскирует номер банковской карты.

python
from src.masks import get_mask_card_number

get_mask_card_number("123456789012)

get_mask_card_number("1234 5678 9012 3456")

get_mask_account(account_number)
Маскирует номер банковского счета.

python
from src.masks import get_mask_account

get_mask_account("12345678901234567890")


get_mask_account("1234567890")

3. Модуль widget — Универсальные функции
mask_account_card(value)
Автоматически определяет тип (карта или счет) и маскирует номер.

python
from src.widget import mask_account_card

mask_account_card("Visa 1234567890123456")


mask_account_card("Счет 12345678901234567890")

get_date(date_string)
Преобразует ISO дату в формат ДД.ММ.ГГГГ.

python
from src.widget import get_date

get_date("2026-08-22T15:30:00")

4. Модуль generators — Генераторы
filter_by_currency(transactions, currency)
Фильтрует транзакции по валюте.

python
from src.generators import filter_by_currency

transactions = [
    {"operationAmount": {"currency": {"code": "USD"}}, "id": 1},
    {"operationAmount": {"currency": {"code": "EUR"}}, "id": 2},
    {"operationAmount": {"currency": {"code": "USD"}}, "id": 3},
]

usd = list(filter_by_currency(transactions, "USD"))
print([t["id"] for t in usd])

transaction_descriptions(transactions)
Возвращает описания транзакций.

python
from src.generators import transaction_descriptions

transactions = [
    {"description": "Payment for services"},
    {"description": "Online purchase"},
]

list(transaction_descriptions(transactions))

card_number_generator(start, end)
Генерирует номера карт в заданном диапазоне.

python
from src.generators import card_number_generator

list(card_number_generator(1, 3))

bash


usd_transactions = filter_by_currency(transactions, "USD")


from transaction_processor import transaction_descriptions

descriptions = transaction_descriptions(transactions)


## Новые функции и генераторы

### Генераторы
- `card_number_generator(length=16)` — генерирует случайный номер карты заданной длины (по умолчанию 16 цифр).
  - Поддерживаемые длины: от 13 до 19 цифр.
  - Возвращает строку из цифр.

### Тестирование
- Реализованы параметризованные тесты для проверки корректности длины и формата номеров карт.




Модуль masks.py - Маскирование данных
Описание
Модуль содержит функции для маскирования конфиденциальных данных: номеров карт и счетов.

Функции
get_mask_card_number(card_number: str) -> str
Маскирует номер банковской карты.

Параметры:

card_number (str): Номер карты (может содержать пробелы, дефисы)

Возвращает:

str: Замаскированный номер карты в формате XXXX XX** **** XXXX

Примеры:

python
from src.masks import get_mask_card_number

# Стандартный номер
get_mask_card_number("1234567890123456")


# Номер с пробелами
get_mask_card_number("1234 5678 9012 3456")


# Номер с дефисами
get_mask_card_number("1234-5678-9012-3456")


# Особенности


Поддерживает номера длиной 13-19 цифр

Корректно обрабатывает номера с разделителями

Возвращает пустую строку для пустого ввода

Сохраняет первые 6 и последние 4 цифры

get_mask_account(account_number: str) -> str
Маскирует номер банковского счета.

Параметры:

account_number (str): Номер счета

Возвращает:

str: Замаскированный номер счета в формате **XXXX

Примеры:

python
from src.masks import get_mask_account

# Стандартный номер счета
get_mask_account("12345678901234567890")


# Короткий номер
get_mask_account("1234567890")


# Номер с пробелами
get_mask_account("1234 5678 9012 3456 7890")



# Особенности

Показывает только последние 4 цифры

Добавляет ** перед последними 4 цифрами

Корректно обрабатывает номера любой длины

Возвращает пустую строку для пустого ввода

Модуль widget.py - Widget функции
Описание
Модуль содержит универсальные функции для обработки данных: маскирование карт/счетов и форматирование дат.

Функции
mask_account_card(value: str) -> str
Универсальная функция маскирования, определяет тип данных автоматически.

Параметры:

value (str): Строка с типом и номером карты или счета

Возвращает:

str: Замаскированный номер

Примеры:

python
from src.widget import mask_account_card

# Маскирование карты
mask_account_card("Visa 1234567890123456")


mask_account_card("MasterCard 1111222233334444")


mask_account_card("МИР 1234567890123456")


# Маскирование счета
mask_account_card("Счет 12345678901234567890")


mask_account_card("Счет 1234567890")


# Обработка ошибок
mask_account_card("Invalid data")

mask_account_card("")
# Особенности


Автоматически определяет тип (карта/счет)

Поддерживает различные типы карт (Visa, MasterCard, Maestro, МИР)

Обрабатывает номера с разделителями

Выбрасывает ValueError для некорректных данных

get_date(date_string: str) -> str
Преобразует дату из ISO формата в формат ДД.ММ.ГГГГ.

Параметры:

date_string (str): Дата в ISO формате

Возвращает:

str: Дата в формате ДД.ММ.ГГГГ

Примеры:

python
from src.widget import get_date

# ISO формат с временем
get_date("2026-08-22T15:30:00")


# ISO формат с временной зоной
get_date("2026-08-22T15:30:00+03:00")


# Только дата
get_date("2026-08-22")

# Особенности

Поддерживает ISO формат с временем

Обрабатывает временные зоны

Возвращает пустую строку для пустых данных

Форматирует дату в российский формат

Модуль processing.py - Обработка транзакций
Описание
Модуль содержит функции для фильтрации и сортировки транзакций.

Функции
filter_by_state(transactions: list[dict], state: str) -> list[dict]
Фильтрует транзакции по заданному статусу.

Параметры:

transactions (list[dict]): Список транзакций

state (str): Статус для фильтрации

Возвращает:

list[dict]: Отфильтрованный список транзакций

Примеры:

python
from src.processing import filter_by_state

transactions = [
    {"id": 1, "state": "EXECUTED"},
    {"id": 2, "state": "PENDING"},
    {"id": 3, "state": "EXECUTED"},
    {"id": 4, "state": "CANCELLED"},
]

# Фильтрация по статусу EXECUTED
executed = filter_by_state(transactions, "EXECUTED")


# Фильтрация по статусу PENDING
pending = filter_by_state(transactions, "PENDING")


# Фильтрация по отсутствующему статусу
cancelled = filter_by_state(transactions, "COMPLETED")


# Пустой список
empty = filter_by_state([], "EXECUTED")

Особенности:

Фильтрует по точному совпадению статуса

Возвращает пустой список для несуществующего статуса

Корректно обрабатывает пустой список

sort_by_date(transactions: list[dict], reverse: bool = True) -> list[dict]
Сортирует транзакции по дате.

Параметры:

transactions (list[dict]): Список транзакций

reverse (bool): Порядок сортировки (True - убывание, False - возрастание)

Возвращает:

list[dict]: Отсортированный список транзакций

Примеры:

python
from src.processing import sort_by_date

transactions = [
    {"id": 1, "date": "2026-08-22T10:00:00"},
    {"id": 2, "date": "2026-08-21T15:30:00"},
    {"id": 3, "date": "2026-08-20T09:15:00"},
]

# Сортировка по убыванию (по умолчанию)
sorted_desc = sort_by_date(transactions)


# Сортировка по возрастанию
sorted_asc = sort_by_date(transactions, reverse=False)



Особенности:

Сортирует по дате в формате ISO

По умолчанию сортирует по убыванию (новые -> старые)

Корректно обрабатывает пустой список

Фикстуры для тестов
python
import pytest

@pytest.fixture
def sample_transactions():
    """Фикстура с тестовыми транзакциями"""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2026-08-22T10:00:00"},
        {"id": 2, "state": "PENDING", "date": "2026-08-21T15:30:00"},
        {"id": 3, "state": "EXECUTED", "date": "2026-08-20T09:15:00"},
        {"id": 4, "state": "CANCELLED", "date": "2026-08-19T18:45:00"},
    ]

@pytest.fixture
def sample_card_numbers():
    """Фикстура с номерами карт"""
    return {
        "valid": "1234567890123456",
        "with_spaces": "1234 5678 9012 3456",
        "with_dashes": "1234-5678-9012-3456",
        "short": "1234",
        "empty": "",
    }

@pytest.fixture
def sample_account_numbers():
    """Фикстура с номерами счетов"""
    return {
        "valid": "12345678901234567890",
        "short": "1234567890",
        "very_short": "1234",
        "empty": "",
    }
Примеры тестов
python
def test_get_mask_card_number_valid(sample_card_numbers):
    """Тест маскирования валидного номера карты"""
    result = get_mask_card_number(sample_card_numbers["valid"])
    assert result == "1234 56** **** 3456"

def test_get_mask_account_valid(sample_account_numbers):
    """Тест маскирования валидного номера счета"""
    result = get_mask_account(sample_account_numbers["valid"])
    assert result == "**7890"

def test_filter_by_state_executed(sample_transactions):
    """Тест фильтрации по статусу EXECUTED"""
    result = filter_by_state(sample_transactions, "EXECUTED")
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)

# Product Catalog

Каталог товаров с классами `Product` и `Category`.

## 📋 Описание

Проект содержит два класса:

- **Product** — описывает товар (название, описание, цена, количество)
- **Category** — описывает категорию товаров (название, описание, список товаров)

##  Отчет по покрытию тестов 

---







```python
from src.masks import get_mask_card_number, get_mask_account

# Маскировка номера карты
get_mask_card_number("1234567890123456")
# Результат: "1234 56** **** 3456"

# Маскировка номера счета
get_mask_account("12345678901234567890")
# Результат: "**7890"
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
src\__init__.py         0      0   100%
src\dates.py           48     25    79%   19-33, 49-63, 84
src\generators.py      38     15    61%   9, 18, 29-34, 42-43, 52-58
src\masks.py           19      1    95%   19
src\processing.py      24      4    83%   10-12, 25
src\widget.py          78     16    79%   4-7, 12-13, 101, 104-105, 123-125, 130-131, 144, 152-153
-------------------------------------------------
TOTAL                 207     61    80%

(.venv) PS C:\Users\User\PycharmProjects\PythonProject5> python -m pytest --cov=src --cov-report=html
======================================================================================================= test session starts =======================================================================================================
platform win32 -- Python 3.12.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\User\PycharmProjects\PythonProject5
configfile: pyproject.toml
plugins: cov-7.1.0
collected 107 items                                                                                                                                                                                                                

tests\test_dates.py ............                                                                                                                                                                                             [ 79%]
tests\test_filters.py ...........                                                                                                                                                                                            [ 61%]
tests\test_masks.py ................                                                                                                                                                                                         [ 95%]
tests\test_processing.py ...........                                                                                                                                                                                         [ 80%]
tests\test_widget.py .....................................................                                                                                                                                                   [ 96%]
tests\tests\test_dates_direct.py ....                                                                                                                                                                                        [100%]

========================================================================================================= tests coverage ==========================================================================================================
_________________________________________________________________________________________ coverage: platform win32, python 3.12.7-final-0 _________________________________________________________________________________________

Coverage HTML written to dir htmlcov
======================================================================================================= 107 passed in 0.63s =======================================================================================================