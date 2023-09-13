from cicd.ios.actions.xcodebuild import TestError, XCBTestAction

from .base_ios import BaseIOSMixin
from .test_sharding import TestShardingMixin


class TestMixin(BaseIOSMixin, TestShardingMixin):
    def start_testing(self):
        def retry_kwargs_fn(kwargs, ctx):
            if isinstance(ctx.error, TestError):
                kwargs['only_testing'] = ctx.error.xcresult.failed_tests
            return kwargs

        shard = self.get_test_shard(**self.kwargs)
        if shard:
            self.kwargs['only_testing'] = shard
        if 'retry_kwargs_fn' not in self.kwargs:
            self.kwargs['retry_kwargs_fn'] = retry_kwargs_fn
        self.runner_exec(action_cls=XCBTestAction)
