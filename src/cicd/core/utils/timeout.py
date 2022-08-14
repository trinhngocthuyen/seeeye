import functools
import signal
import typing as t


class Timeout:
    class TimeoutError(Exception):
        pass

    def __init__(self, seconds: int, func: t.Optional[callable] = None) -> None:
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


T = t.TypeVar('T')


def timeout(seconds: int) -> t.Callable[[t.Callable[..., T]], t.Callable[..., T]]:
    def decorator(func: t.Callable[..., T]):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with Timeout(seconds=seconds, func=func):
                return func(*args, **kwargs)

        return wrapper

    return decorator
