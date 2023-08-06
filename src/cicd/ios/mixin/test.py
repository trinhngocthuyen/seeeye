from cicd.ios.actions.xcodebuild import XCBTestAction

from .base_ios import BaseIOSMixin
from .test_sharding import TestShardingMixin


class TestMixin(BaseIOSMixin, TestShardingMixin):
    def start_testing(self):
        shard = self.get_test_shard(**self.kwargs)
        if shard:
            self.kwargs['only_testing'] = shard
        self.runner_exec(action_cls=XCBTestAction)
