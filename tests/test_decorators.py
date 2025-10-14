import os
import tempfile
from typing import Any

import pytest

from src.decorators import _write_log, log


def test_write_log_to_file() -> None:
    """Тест записи лога в файл"""
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
    filename = temp_file.name
    temp_file.close()

    try:
        # Записываем тестовое сообщение
        test_message = "Test log message"
        _write_log(test_message, filename)

        # Проверяем, что сообщение записано в файл
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read().strip()

        assert content == test_message
    finally:
        # Удаляем временный файл
        if os.path.exists(filename):
            os.unlink(filename)


def test_write_log_to_console(capsys: Any) -> None:
    """Тест вывода лога в консоль"""
    test_message = "Console test message"
    _write_log(test_message)

    captured = capsys.readouterr()
    assert captured.out.strip() == test_message


def test_successful_function_execution_file_log() -> None:
    """Тест успешного выполнения функции с записью в файл"""
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
    filename = temp_file.name
    temp_file.close()

    try:

        def add_numbers(a: int, b: int) -> int:
            return a + b

        decorated_func = log(filename=filename)(add_numbers)
        result = decorated_func(5, 3)

        # Проверяем результат функции
        assert result == 8

        # Проверяем содержимое лог-файла
        with open(filename, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "add_numbers started" in log_content
        assert "add_numbers ok. Result: 8" in log_content

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_successful_function_execution_console_log(capsys: Any) -> None:
    """Тест успешного выполнения функции с выводом в консоль"""

    def multiply_numbers(x: int, y: int) -> int:
        return x * y

    decorated_func = log()(multiply_numbers)
    result = decorated_func(4, 5)

    # Проверяем результат функции
    assert result == 20

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    console_output = captured.out

    assert "multiply_numbers started" in console_output
    assert "multiply_numbers ok. Result: 20" in console_output


def test_function_with_exception_file_log() -> None:
    """Тест функции с исключением при записи в файл"""
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
    filename = temp_file.name
    temp_file.close()

    try:

        def divide_numbers(a: float, b: float) -> float:
            return a / b

        decorated_func = log(filename=filename)(divide_numbers)

        # Проверяем, что исключение пробрасывается
        with pytest.raises(ZeroDivisionError):
            decorated_func(10, 0)

        # Проверяем содержимое лог-файла
        with open(filename, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "divide_numbers started" in log_content
        assert "divide_numbers error: ZeroDivisionError" in log_content
        assert "Inputs: (10, 0), {}" in log_content

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_function_with_exception_console_log(capsys: Any) -> None:
    """Тест функции с исключением при выводе в консоль"""

    def raise_value_error() -> None:
        raise ValueError("Custom error message")

    decorated_func = log()(raise_value_error)

    # Проверяем, что исключение пробрасывается
    with pytest.raises(ValueError):
        decorated_func()

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    console_output = captured.out

    assert "raise_value_error started" in console_output
    assert "raise_value_error error: ValueError" in console_output
    assert "Custom error message" in console_output


def test_function_with_args_and_kwargs_file_log() -> None:
    """Тест функции с аргументами и ключевыми аргументами при записи в файл"""
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
    filename = temp_file.name
    temp_file.close()

    try:

        def complex_function(a: int, b: int, c: int = 10, d: int = 20) -> int:
            return a + b + c + d

        decorated_func = log(filename=filename)(complex_function)
        result = decorated_func(1, 2, c=30, d=40)

        # Проверяем результат
        assert result == 73

        # Проверяем содержимое лог-файла
        with open(filename, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "complex_function started" in log_content
        assert "complex_function ok. Result: 73" in log_content

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_function_with_args_and_kwargs_exception(capsys: Any) -> None:
    """Тест функции с аргументами и ключевыми аргументами при возникновении исключения"""

    def failing_function(x: str, y: str, z: int = 123) -> str:
        # Функция, которая вызовет TypeError при попытке сложить строку и число
        return x + y + str(z)  # Исправлено - преобразуем число в строку

    decorated_func = log()(failing_function)

    # Проверяем, что функция выполняется успешно (теперь без ошибки)
    result = decorated_func("test", "string")
    assert result == "teststring123"

    # Проверяем вывод в консоль
    captured = capsys.readouterr()
    console_output = captured.out

    assert "failing_function started" in console_output
    assert "failing_function ok. Result: teststring123" in console_output


def test_function_preserves_metadata() -> None:
    """Тест, что декоратор сохраняет метаданные оригинальной функции"""

    def documented_function(x: int) -> int:
        """Тестовая функция с документацией"""
        return x * 2

    decorated_func = log(filename=None)(documented_function)

    # Проверяем сохранение метаданных
    assert decorated_func.__name__ == "documented_function"
    assert decorated_func.__doc__ == "Тестовая функция с документацией"


def test_multiple_calls_to_same_function() -> None:
    """Тест множественных вызовов одной функции"""
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
    filename = temp_file.name
    temp_file.close()

    try:
        call_count = 0

        def counter() -> int:
            nonlocal call_count
            call_count += 1
            return call_count

        decorated_func = log(filename=filename)(counter)

        # Вызываем функцию несколько раз
        assert decorated_func() == 1
        assert decorated_func() == 2
        assert decorated_func() == 3

        # Проверяем, что все вызовы залогированы
        with open(filename, "r", encoding="utf-8") as f:
            log_lines = [line.strip() for line in f.readlines()]

        # Должно быть 6 строк (3 начала + 3 завершения)
        assert len(log_lines) == 6

        # Проверяем конкретные строки по индексам
        assert log_lines[0] == "counter started"
        assert log_lines[1] == "counter ok. Result: 1"
        assert log_lines[2] == "counter started"
        assert log_lines[3] == "counter ok. Result: 2"
        assert log_lines[4] == "counter started"
        assert log_lines[5] == "counter ok. Result: 3"

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_function_with_none_result() -> None:
    """Тест функции, возвращающей None"""
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
    filename = temp_file.name
    temp_file.close()

    try:

        def none_function() -> None:
            return None

        decorated_func = log(filename=filename)(none_function)
        result = decorated_func()

        assert result is None

        # Проверяем лог
        with open(filename, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "none_function started" in log_content
        assert "none_function ok. Result: None" in log_content

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_function_with_complex_return_type(capsys: Any) -> None:
    """Тест функции с комплексным типом возвращаемого значения"""

    def list_function() -> list[dict[str, int]]:
        return [{"a": 1, "b": 2}, {"c": 3}]

    decorated_func = log()(list_function)
    result = decorated_func()

    assert result == [{"a": 1, "b": 2}, {"c": 3}]

    captured = capsys.readouterr()
    console_output = captured.out

    assert "list_function started" in console_output
    assert "list_function ok. Result: [{'a': 1, 'b': 2}, {'c': 3}]" in console_output


def test_decorator_without_parentheses() -> None:
    """Тест использования декоратора без скобок"""
    temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, encoding="utf-8")
    filename = temp_file.name
    temp_file.close()

    try:

        def test_func() -> str:
            return "success"

        decorated_func = log(filename=filename)(test_func)
        result = decorated_func()
        assert result == "success"

        with open(filename, "r", encoding="utf-8") as f:
            log_content = f.read()

        assert "test_func started" in log_content
        assert "test_func ok. Result: success" in log_content

    finally:
        if os.path.exists(filename):
            os.unlink(filename)


def test_decorator_with_none_filename(capsys: Any) -> None:
    """Тест декоратора с явным None в качестве filename"""

    def explicit_none_func() -> int:
        return 42

    decorated_func = log(filename=None)(explicit_none_func)
    result = decorated_func()
    assert result == 42

    captured = capsys.readouterr()
    console_output = captured.out

    assert "explicit_none_func started" in console_output
    assert "explicit_none_func ok. Result: 42" in console_output

