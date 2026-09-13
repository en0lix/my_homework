import os
import tempfile
from typing import Any, Dict, List, Optional

import pytest

from src.decorators import log

# ==================== ТЕСТЫ ДЛЯ ЛОГИРОВАНИЯ В ФАЙЛ ====================


class TestLogToFile:
    """Тесты для декоратора log с записью в файл."""

    def test_log_success_to_file(self) -> None:
        """Тест логирования успешного выполнения в файл."""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp_file:
            filename = tmp_file.name

        try:

            @log(filename=filename)
            def add(a: int, b: int) -> int:
                return a + b

            result = add(2, 3)
            assert result == 5

            # Проверяем содержимое файла
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                assert content == "add ok"

        finally:
            # Удаляем временный файл
            if os.path.exists(filename):
                os.remove(filename)

    def test_log_error_to_file(self) -> None:
        """Тест логирования ошибки в файл."""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp_file:
            filename = tmp_file.name

        try:

            @log(filename=filename)
            def divide(a: int, b: int) -> float:
                return a / b

            with pytest.raises(ZeroDivisionError):
                divide(10, 0)

            # Проверяем содержимое файла
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                assert "divide error: ZeroDivisionError" in content
                assert "Inputs: (10, 0)" in content

        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_log_with_kwargs_to_file(self) -> None:
        """Тест логирования с именованными аргументами."""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp_file:
            filename = tmp_file.name

        try:

            @log(filename=filename)
            def greet(name: str, age: int) -> str:
                return f"Hello, {name}!"

            result = greet(name="Alice", age=30)
            assert result == "Hello, Alice!"

            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                assert content == "greet ok"

        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_log_multiple_calls_to_file(self) -> None:
        """Тест множественных вызовов функции с логированием."""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp_file:
            filename = tmp_file.name

        try:

            @log(filename=filename)
            def multiply(a: int, b: int) -> int:
                return a * b

            multiply(2, 3)
            multiply(4, 5)
            multiply(6, 7)

            with open(filename, "r", encoding="utf-8") as f:
                lines = f.read().strip().split("\n")
                assert len(lines) == 3
                assert all(line == "multiply ok" for line in lines)

        finally:
            if os.path.exists(filename):
                os.remove(filename)


# ==================== ТЕСТЫ ДЛЯ ЛОГИРОВАНИЯ В КОНСОЛЬ ====================


class TestLogToConsole:
    """Тесты для декоратора log с выводом в консоль."""

    def test_log_success_to_console(self, capsys: Any) -> None:
        """Тест логирования успешного выполнения в консоль."""

        @log()
        def subtract(a: int, b: int) -> int:
            return a - b

        result = subtract(10, 4)
        assert result == 6

        captured = capsys.readouterr()
        assert "subtract ok" in captured.out

    def test_log_error_to_console(self, capsys: Any) -> None:
        """Тест логирования ошибки в консоль."""

        @log()
        def divide(a: int, b: int) -> float:
            return a / b

        with pytest.raises(ZeroDivisionError):
            divide(10, 0)

        captured = capsys.readouterr()
        assert "divide error: ZeroDivisionError" in captured.out
        assert "Inputs: (10, 0)" in captured.out

    def test_log_with_kwargs_to_console(self, capsys: Any) -> None:
        """Тест логирования с именованными аргументами в консоль."""

        @log()
        def create_user(name: str, age: int, active: bool = True) -> Dict[str, Any]:
            return {"name": name, "age": age, "active": active}

        result = create_user(name="Bob", age=25, active=False)
        assert result["name"] == "Bob"

        captured = capsys.readouterr()
        assert "create_user ok" in captured.out

    def test_log_multiple_calls_to_console(self, capsys: Any) -> None:
        """Тест множественных вызовов с логированием в консоль."""

        @log()
        def add(a: int, b: int) -> int:
            return a + b

        add(1, 2)
        add(3, 4)
        add(5, 6)

        captured = capsys.readouterr()
        lines = [line.strip() for line in captured.out.strip().split("\n")]
        assert len(lines) == 3
        assert all(line == "add ok" for line in lines)


# ==================== ТЕСТЫ ДЛЯ РАЗНЫХ ТИПОВ ФУНКЦИЙ ====================


class TestLogWithDifferentFunctions:
    """Тесты для декоратора log с разными типами функций."""

    def test_log_with_string_function(self, capsys: Any) -> None:
        """Тест логирования функции, возвращающей строку."""

        @log()
        def get_message(name: str) -> str:
            return f"Hello, {name}!"

        result = get_message("World")
        assert result == "Hello, World!"

        captured = capsys.readouterr()
        assert "get_message ok" in captured.out

    def test_log_with_list_function(self, capsys: Any) -> None:
        """Тест логирования функции, возвращающей список."""

        @log()
        def get_numbers(n: int) -> List[int]:
            return list(range(n))

        result = get_numbers(5)
        assert result == [0, 1, 2, 3, 4]

        captured = capsys.readouterr()
        assert "get_numbers ok" in captured.out

    def test_log_with_empty_args(self, capsys: Any) -> None:
        """Тест логирования функции без аргументов."""

        @log()
        def say_hello() -> str:
            return "Hello!"

        result = say_hello()
        assert result == "Hello!"

        captured = capsys.readouterr()
        assert "say_hello ok" in captured.out

    def test_log_with_multiple_exceptions(self) -> None:
        """Тест логирования разных типов исключений."""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".txt") as tmp_file:
            filename = tmp_file.name

        try:

            @log(filename=filename)
            def risky_operation(value: int) -> int:
                if value < 0:
                    raise ValueError("Negative value")
                if value == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                return 100 // value

            with pytest.raises(ValueError):
                risky_operation(-5)

            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                assert "risky_operation error: ValueError" in content
                assert "Inputs: (-5,)" in content

            # Очищаем файл для следующего вызова
            with open(filename, "w", encoding="utf-8") as f:
                f.write("")

            with pytest.raises(ZeroDivisionError):
                risky_operation(0)

            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                assert "risky_operation error: ZeroDivisionError" in content
                assert "Inputs: (0,)" in content

        finally:
            if os.path.exists(filename):
                os.remove(filename)


# ==================== ТЕСТЫ ДЛЯ РАЗНЫХ СЦЕНАРИЕВ ====================


class TestLogScenarios:
    """Тесты для различных сценариев использования декоратора log."""

    def test_log_preserves_function_metadata(self) -> None:
        """Тест сохранения метаданных функции."""

        @log()
        def test_function(a: int, b: int) -> int:
            """Test function docstring."""
            return a + b

        assert test_function.__name__ == "test_function"
        assert test_function.__doc__ == "Test function docstring."

    def test_log_with_different_filename_extensions(self) -> None:
        """Тест с разными расширениями файлов."""
        extensions = [".log", ".txt", ".out"]

        for ext in extensions:
            with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=ext) as tmp_file:
                filename = tmp_file.name

            try:

                @log(filename=filename)
                def test_func() -> str:
                    return "test"

                test_func()

                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    assert content == "test_func ok"

            finally:
                if os.path.exists(filename):
                    os.remove(filename)

    def test_log_exception_with_complex_args(self, capsys: Any) -> None:
        """Тест логирования ошибки со сложными аргументами."""

        @log()
        def process_data(data: Dict[str, Any], items: List[int]) -> int:
            if not items:
                raise ValueError("Empty list")
            return sum(items)

        with pytest.raises(ValueError):
            process_data({"key": "value"}, [])

        captured = capsys.readouterr()
        assert "process_data error: ValueError" in captured.out
        assert "Inputs: ({'key': 'value'}, [])" in captured.out
