from typing import Optional

from cicd.ios.runner.xcodebuild import XCBTestRunner


class TestMixin:
    def start_testing(self, **kwargs):
        runner = XCBTestRunner()
        runner.run(**kwargs)
