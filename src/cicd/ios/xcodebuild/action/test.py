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
    xcresult: XCResult

    def run(self) -> XCResult:
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
