
from .base import XCBAction


class ArchiveError(Exception):
    pass


class XCBArchiveAction(XCBAction):
    '''A class that interacts with the xcodebuild command, particularly for archive actions.'''

    def run(self):
        kwargs = self.kwargs
        try:
            if not kwargs.get('actions'):
                kwargs['actions'] = ['archive']
            with self.collect_xcarchives():
                return super().run()
        except Exception as e:
            raise ArchiveError(e)
