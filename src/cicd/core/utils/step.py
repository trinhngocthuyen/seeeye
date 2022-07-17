import time
from contextlib import contextmanager

from cicd.core.logger import logger


@contextmanager
def step(name: str, **kwargs):
    prefix = kwargs.get('prefix', 'Step:')
    tick = time.time()
    logger.info(f'⇣ {prefix} {name} (started)')
    yield
    timespent = int(time.time() - tick)
    logger.info(f'⇢ {prefix} {name} (finished) ({timespent} s)')
