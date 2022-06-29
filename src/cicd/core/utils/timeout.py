import functools
import signal
from typing import Callable, Optional, TypeVar


class Timeout:
    class TimeoutError(Exception):
        pass

    def __init__(self, seconds: int, func: Optional[callable] = None) -> None:
        self.seconds = seconds
        self.func = func

    def __enter__(self):
        def handler(signum, frame):
            raise TimeoutError(
                f'Function <{self.func}> timed out after {self.seconds} (s)'
            )

        signal.signal(signal.SIGALRM, handler=handler)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)


T = TypeVar('T')


def timeout(seconds: int) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with Timeout(seconds=seconds, func=func):
                return func(*args, **kwargs)

        return wrapper

    return decorator
