"""
Тесты для классов Product и Category.
"""

import pytest

from src.product_catalog.models import Category, Product


class TestProduct:
    """Тесты для класса Product."""

    def test_product_creation(self) -> None:
        """Тест создания товара."""
        product = Product("iPhone", "Смартфон Apple", 99999.99, 10)

        assert product.name == "iPhone"
        assert product.description == "Смартфон Apple"
        assert product.price == 99999.99
        assert product.quantity == 10

    def test_product_types(self) -> None:
        """Тест типов атрибутов товара."""
        product = Product("iPhone", "Смартфон", 99999.99, 10)

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)

    def test_product_price_conversion(self) -> None:
        """Тест приведения цены к float."""
        product = Product("iPhone", "Смартфон", "99999.99", "10")

        assert product.price == 99999.99
        assert product.quantity == 10

    def test_product_repr(self) -> None:
        """Тест строкового представления."""
        product = Product("iPhone", "Смартфон", 99999.99, 10)
        repr_str = repr(product)

        assert "iPhone" in repr_str
        assert "Смартфон" in repr_str
        assert "99999.99" in repr_str


class TestCategory:
    """Тесты для класса Category."""

    def test_category_creation(self) -> None:
        """Тест создания категории."""
        products = [
            Product("iPhone", "Смартфон", 99999.99, 10),
            Product("Samsung", "Смартфон", 79999.99, 5),
        ]
        category = Category("Смартфоны", "Мобильные телефоны", products)

        assert category.name == "Смартфоны"
        assert category.description == "Мобильные телефоны"
        assert len(category.products) == 2
        assert category.products_count == 2

    def test_category_products_is_list(self) -> None:
        """Тест, что products — это список."""
        products = [Product("iPhone", "Смартфон", 99999.99, 10)]
        category = Category("Смартфоны", "Мобильные телефоны", products)

        assert isinstance(category.products, list)

    def test_category_products_are_products(self) -> None:
        """Тест, что в products только объекты Product."""
        products = [
            Product("iPhone", "Смартфон", 99999.99, 10),
            Product("Samsung", "Смартфон", 79999.99, 5),
        ]
        category = Category("Смартфоны", "Мобильные телефоны", products)

        for product in category.products:
            assert isinstance(product, Product)

    def test_category_empty_products(self) -> None:
        """Тест пустой категории."""
        category = Category("Пустая", "Без товаров", [])

        assert category.products == []
        assert category.products_count == 0

    def test_category_none_products(self) -> None:
        """Тест категории с None вместо списка."""
        category = Category("Пустая", "Без товаров", None)  # type: ignore

        assert category.products == []
        assert category.products_count == 0

    def test_category_repr(self) -> None:
        """Тест строкового представления."""
        category = Category("Смартфоны", "Мобильные телефоны", [])
        repr_str = repr(category)

        assert "Смартфоны" in repr_str
        assert "Мобильные телефоны" in repr_str
