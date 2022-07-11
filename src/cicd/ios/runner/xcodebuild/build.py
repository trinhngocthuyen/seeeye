from functools import cached_property

from cicd.ios.runner.base import Runner
from cicd.ios.xcodebuild.action import XCBBuildAction


class XCBBuildRunner(Runner):
    @cached_property
    def action(self):
        return XCBBuildAction()
