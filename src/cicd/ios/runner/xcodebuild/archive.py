from cicd.ios.actions.xcodebuild import XCBArchiveAction
from cicd.ios.runner.base import Runner


class XCBArchiveRunner(Runner):
    '''A (runner) class to archive an iOS project (backed by ``XCBArchiveAction``).'''

    @property
    def action_cls(self):
        return XCBArchiveAction
