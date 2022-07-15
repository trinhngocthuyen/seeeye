from functools import cached_property

from cicd.ios.runner.base import Runner
from cicd.ios.xcodebuild.action import TestError, XCBTestAction


class XCBTestRunner(Runner):
    @cached_property
    def action(self):
        return XCBTestAction()

    def run(self, **kwargs):
        def retry_kwargs_fn(kwargs: dict, ctx: Runner.RetryContext):
            if isinstance(ctx.error, TestError):
                kwargs['only_testing'] = ctx.error.xcresult.failed_tests
            return kwargs

        kwargs['retry_kwargs_fn'] = retry_kwargs_fn
        return super().run(**kwargs)
