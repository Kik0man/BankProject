import functools
from typing import Any, Optional


def log(filename: Optional[str] = None) -> Any:
    """
    Декоратор для логирования начала и конца выполнения функции, а также результатов или ошибок.
    """

    def decorator(func: Any) -> Any:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Логируем начало выполнения
            start_message = f"{func.__name__} started"
            _write_log(start_message, filename)

            try:
                # Выполняем функцию
                result = func(*args, **kwargs)

                # Логируем успешное завершение
                success_message = f"{func.__name__} ok. Result: {result}"
                _write_log(success_message, filename)

                return result

            except Exception as e:
                # Логируем ошибку
                error_message = f"{func.__name__} error: {type(e).__name__}: {str(e)}. " f"Inputs: {args}, {kwargs}"
                _write_log(error_message, filename)
                raise

        return wrapper

    return decorator


def _write_log(message: str, filename: Optional[str] = None) -> None:
    """Вспомогательная функция для записи лога в файл или консоль."""

    if filename:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    else:
        print(message)
