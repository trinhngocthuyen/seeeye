from cicd.ios.actions.xcodebuild import XCBBuildAction
from cicd.ios.runner.base import Runner


class XCBBuildRunner(Runner):
    '''A (runner) class to build an iOS project (backed by ``XCBuildAction``)'''

    @property
    def action_cls(self):
        return XCBBuildAction
