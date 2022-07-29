from cicd.ios.actions.xcodebuild import TestError, XCBTestAction
from cicd.ios.runner.base import Runner


class XCBTestRunner(Runner):
    '''A (runner) class to test an iOS project (backed by ``XCTestAction``).'''

    @property
    def action_cls(self):
        return XCBTestAction

    def run(self, **kwargs):
        def retry_kwargs_fn(kwargs: dict, ctx: Runner.RetryContext):
            if isinstance(ctx.error, TestError):
                kwargs['only_testing'] = ctx.error.xcresult.failed_tests
            return kwargs

        kwargs['retry_kwargs_fn'] = retry_kwargs_fn
        return super().run(**kwargs)
