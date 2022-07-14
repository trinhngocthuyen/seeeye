from cicd.ios.runner.xcodebuild import XCBTestRunner

from .base_ios import BaseIOSMixin


class TestMixin(BaseIOSMixin):
    def start_testing(self, **kwargs):
        self.pre_run(**kwargs)
        runner = XCBTestRunner()
        runner.run(**kwargs)
        self.post_run(**kwargs)
