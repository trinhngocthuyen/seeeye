from cicd.ios.runner.xcodebuild import XCBTestRunner

from .base_ios import BaseIOSMixin


class TestMixin(BaseIOSMixin):
    def start_testing(self, **kwargs):
        with self.step('pre-run'):
            self.pre_run(**kwargs)

        with self.step('run'):
            runner = XCBTestRunner()
            runner.run(**kwargs)

        with self.step('post-run'):
            self.post_run(**kwargs)
