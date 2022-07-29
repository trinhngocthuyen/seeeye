from cicd.ios.runner.base import Runner
from cicd.ios.xcodebuild.action import XCBBuildAction


class XCBBuildRunner(Runner):
    '''A (runner) class to build an iOS project (backed by ``XCBuildAction``)'''

    @property
    def action_cls(self):
        return XCBBuildAction
