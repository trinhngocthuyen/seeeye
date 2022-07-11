from functools import cached_property

from cicd.ios.runner.base import Runner
from cicd.ios.xcodebuild.action import XCBTestAction


class XCBTestRunner(Runner):
    @cached_property
    def action(self):
        return XCBTestAction()
