from cicd.ios.runner.xcodebuild import XCBTestRunner

from .base_ios import BaseIOSMixin
from .test_sharding import TestShardingMixin


class TestMixin(BaseIOSMixin, TestShardingMixin):
    def start_testing(self):
        with self.step('pre-run'):
            self.pre_run()

        with self.step('run'):
            runner = XCBTestRunner()
            kwargs = self.kwargs.copy()
            shard = self.get_test_shard(**kwargs)
            if shard:
                kwargs['only_testing'] = shard
            runner.run(**kwargs)

        with self.step('post-run'):
            self.post_run()
