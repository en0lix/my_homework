"""
Модуль models содержит классы Product и Category для каталога товаров.
"""

from typing import List


class Product:
    """
    Класс Product описывает товар в каталоге.

    Атрибуты:
        name (str): Название товара.
        description (str): Описание товара.
        price (float): Цена товара.
        quantity (int): Количество в наличии.
    """

    # Классовый атрибут — общее количество продуктов
    products_count: int = 0

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """
        Инициализирует товар.

        Args:
            name: Название товара.
            description: Описание товара.
            price: Цена товара.
            quantity: Количество в наличии.
        """
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = int(quantity)

        # Увеличиваем общий счётчик продуктов
        Product.products_count += 1

    def __repr__(self) -> str:
        """Строковое представление товара."""
        return (
            f"Product(name={self.name!r}, description={self.description!r}, "
            f"price={self.price}, quantity={self.quantity})"
        )


class Category:
    """
    Класс Category описывает категорию товаров.

    Атрибуты:
        name (str): Название категории.
        description (str): Описание категории.
        products (List[Product]): Список товаров категории.
    """

    # Классовые атрибуты — счётчики
    categories_count: int = 0
    products_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        """
        Инициализирует категорию.

        Args:
            name: Название категории.
            description: Описание категории.
            products: Список товаров категории.
        """
        self.name = name
        self.description = description
        self.products = list(products) if products else []

        # Увеличиваем общий счётчик категорий
        Category.categories_count += 1

        # Считаем количество продуктов в этой категории
        self.products_count = len(self.products)

        # Увеличиваем общий счётчик продуктов на количество в категории
        Category.products_count += len(self.products)

    def __repr__(self) -> str:
        """Строковое представление категории."""
        return (
            f"Category(name={self.name!r}, description={self.description!r}, "
            f"products={self.products!r})"
        )
