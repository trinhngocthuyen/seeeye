from cicd.ios.runner.base import Runner
from cicd.ios.xcodebuild.action import XCBBuildAction


class XCBBuildRunner(Runner):
    @property
    def action_cls(self):
        return XCBBuildAction
