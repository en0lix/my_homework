"""
Модуль decorators содержит декораторы для логирования выполнения функций.
"""

import functools
import logging
import sys
from typing import Any, Callable, Optional, TypeVar, cast

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

            # Очищаем старые обработчики
            if logger.hasHandlers():
                logger.handlers.clear()

            # Создаем обработчик
            if filename:
                handler: logging.Handler = logging.FileHandler(filename, encoding="utf-8")
            else:
                handler = logging.StreamHandler(sys.stdout)

            handler.setLevel(logging.INFO)
            formatter = logging.Formatter("%(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            try:
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} ok")
                return result

            except Exception as e:
                args_str = ", ".join(repr(a) for a in args)
                kwargs_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())

                if kwargs:
                    inputs = f"({args_str}, {kwargs_str})"
                else:
                    inputs = f"({args_str})" if args else "()"

                logger.error(f"{func.__name__} error: {type(e).__name__}. Inputs: {inputs}")
                raise

        return cast(F, wrapper)

    return decorator
