from time import perf_counter_ns
from typing import Callable


def timeit(func: Callable):
    def wrapper(*args, **kwargs):
        start = perf_counter_ns()
        result = func(*args, **kwargs)
        dt = perf_counter_ns() - start
        func_name = f"{func.__module__}.{func.__qualname__}"
        print(f"{func_name} took {dt / 1000000}ms")
        return result

    return wrapper
