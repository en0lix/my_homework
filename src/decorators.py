"""
Модуль decorators содержит декораторы для логирования выполнения функций.
"""

import functools
import logging
import sys
from typing import Any, Callable, Optional, TypeVar, Union

# Тип для функции, возвращающей Any
F = TypeVar("F", bound=Callable[..., Any])


def log(filename: Optional[str] = None) -> Callable[[F], F]:
    """
    Декоратор для логирования выполнения функции.

    Args:
        filename: Имя файла для записи логов. Если не указан, логи выводятся в консоль.

    Returns:
        Callable: Декорированная функция
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Настройка логирования
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)

            # Очищаем старые обработчики, чтобы избежать дублирования
            if logger.hasHandlers():
                logger.handlers.clear()

            # Создаем обработчик (исправлено: используем один тип)
            if filename:
                handler = logging.FileHandler(filename, encoding="utf-8")
            else:
                handler = logging.StreamHandler(sys.stdout)  # type: ignore

            handler.setLevel(logging.INFO)
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное выполнение
                logger.info(f"{func.__name__} ok")

                return result

            except Exception as e:
                # Логируем ошибку с параметрами
                args_str = ", ".join(repr(a) for a in args)
                kwargs_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())

                if kwargs:
                    inputs = f"({args_str}, {kwargs_str})"
                else:
                    inputs = f"({args_str})" if args else "()"

                logger.error(f"{func.__name__} error: {type(e).__name__}. Inputs: {inputs}")

                # Пробрасываем исключение дальше
                raise

        return wrapper  # type: ignore

    return decorator
