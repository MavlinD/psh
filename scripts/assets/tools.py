import functools
from typing import Callable, Any
import time

from logrich.logger_ import log


def timer(func: Callable) -> Callable:
    """декоратор, определяет время выполнения"""

    @functools.wraps(func)
    def wrapper_timer(*args: Any, **kwargs: Any) -> str:
        name = func.__name__
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        format_time = f"{elapsed_time:0.3f} seconds"
        log.info(f"[bold]{name}:[/] {format_time}")
        return value

    return wrapper_timer
