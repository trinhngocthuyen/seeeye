from cicd.ios.syntax.xcresult import XCResult

from .base import XCBAction


class TestError(Exception):
    __test__ = False

    def __init__(self, xcresult: XCResult, *args: object) -> None:
        super().__init__(*args)
        self.xcresult = xcresult


class XCBTestAction(XCBAction):
    '''A class that interacts with the xcodebuild command, particularly for test actions.'''

    def run(self) -> XCResult:
        '''Execute the action

        :raises: The ``TestError`` embedding the xcresult of the test session.
        :return: The ``XCResult`` object corresponding to the test session.
        :rtype: XCResult
        '''

        kwargs = self.kwargs
        try:
            if not kwargs.get('actions'):
                if kwargs.get('test_without_building'):
                    kwargs['actions'] = ['test-without-building']
                else:
                    kwargs['actions'] = ['test']
            with self.collect_xcresults():
                super().run()
            return self.xcresult
        except Exception as e:
            raise TestError(self.xcresult, e)
