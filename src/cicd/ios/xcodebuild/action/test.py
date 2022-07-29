from contextlib import contextmanager
from pathlib import Path
from typing import List

from cicd.core.logger import logger
from cicd.ios.syntax.xcresult import XCResult

from .base import XCBAction


class TestError(Exception):
    __test__ = False

    def __init__(self, xcresult: XCResult, *args: object) -> None:
        super().__init__(*args)
        self.xcresult = xcresult


class XCBTestAction(XCBAction):
    '''A class that iteracts with the xcodebuild command,
    particularly for test actions.
    '''

    xcresult: XCResult

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

    def xcresult_paths(self) -> List[Path]:
        return list(self.derived_data_path.glob('Logs/Test/*.xcresult'))

    @contextmanager
    def collect_xcresults(self):
        '''Collect the xcresults generated after an action.'''
        before = self.xcresult_paths()
        try:
            yield
        finally:
            after = self.xcresult_paths()
            paths = list(set(after).difference(before))
            if len(paths) == 0:
                raise RuntimeError(
                    f'Cannot detect any xcresult bundle. DerivedData: {self.derived_data_path}'
                )
            elif len(paths) > 1:
                logger.warning(f'Detected more than one xcresult bundle: {paths}')
            else:
                logger.info(f'Detected xcresult bundles: {paths}')
            self.xcresult = XCResult(path=paths[0])
