from typing import Optional

from retry import retry

from cicd.core.logger import logger
from cicd.core.utils.timeout import timeout


class Runner:
    class RetryContext(dict):
        @property
        def idx(self) -> int:
            return self.get('idx', 0)

        @property
        def error(self) -> Optional[Exception]:
            return self.get('error')

    def run(self, **kwargs):
        timeout_in_sec = kwargs.get('timeout')
        tries = (kwargs.get('retries') or 0) + 1
        retry_kwargs_fn = kwargs.get('retry_kwargs_fn')
        ctx = Runner.RetryContext()

        @retry(tries=tries, logger=logger)
        def run_without_timeout():
            if callable(retry_kwargs_fn):
                retry_kwargs = retry_kwargs_fn(kwargs, ctx)
            else:
                retry_kwargs = kwargs

            try:
                return self.action.run(**retry_kwargs)
            except Exception as e:
                ctx['error'] = e
                raise e
            finally:
                ctx['idx'] = ctx.idx + 1

        if not self.action:
            return
        if not timeout_in_sec:
            return run_without_timeout()

        @timeout(timeout_in_sec)
        def run_with_timeout():
            return run_without_timeout()

        return run_with_timeout()

    @property
    def action(self):
        pass
