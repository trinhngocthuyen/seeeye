import typing as t

from retry import retry

from cicd.core.action import Action
from cicd.core.logger import logger
from cicd.core.utils.timeout import timeout


class Runner:
    '''A class that wraps the execution of actions.

    A runner executes the backed action under the hood. It adds some extensions
    to the execution such as timeout, retries, etc.

    :param timeout: The timeout in seconds of the runner execution.
    :param retries: The number of action retries.
    :param retry_kwargs_fn: The function to update the ``kwargs`` in the retry.
    :type retry_kwargs_fn: t.Callable[[t.Dict[str, t.Any], RetryContext], t.Dict[str, t.Any]]
    '''

    class RetryContext(dict):
        '''Intermediate data passed around retries.'''

        @property
        def idx(self) -> int:
            return self.get('idx', 0)

        @property
        def error(self) -> t.Optional[Exception]:
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

            action = self.action_cls(**retry_kwargs)

            try:
                return action.run()
            except Exception as e:
                ctx['error'] = e
                raise e
            finally:
                ctx['idx'] = ctx.idx + 1

        if not timeout_in_sec:
            return run_without_timeout()

        @timeout(timeout_in_sec)
        def run_with_timeout():
            return run_without_timeout()

        return run_with_timeout()

    @property
    def action_cls(self) -> t.Type[Action]:
        raise NotImplementedError
