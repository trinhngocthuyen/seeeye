from .base import XCBAction


class XCBArchiveAction(XCBAction):
    '''A class that interacts with the xcodebuild command, particularly for archive actions.'''

    def run(self):
        raise NotImplementedError
