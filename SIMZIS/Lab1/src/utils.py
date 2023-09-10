import time

from functools import wraps

from typing import Callable


def log_time_decorator(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        print(f"Функция {func.__name__} выполнилась за {execution_time} сек.")
        return result

    return wrapper
