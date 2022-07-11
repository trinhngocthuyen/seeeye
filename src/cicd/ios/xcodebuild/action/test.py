from pathlib import Path

from cicd.core.logger import logger
from cicd.ios.syntax.xcresult import XCResult

from .base import XCBAction


class TestError(Exception):
    def __init__(self, xcresult: XCResult, *args: object) -> None:
        super().__init__(*args)
        self.xcresult = xcresult


class XCBTestAction(XCBAction):
    def run(self, **kwargs) -> XCResult:
        def _xcresult_paths():
            return set(self._derived_data_path(**kwargs).glob('Logs/Test/*.xcresult'))

        xcresult_paths_before = _xcresult_paths()

        def collect_xcresult():
            paths = list(_xcresult_paths().difference(xcresult_paths_before))
            if not paths:
                raise RuntimeError('Cannot detect any xcresult bundle')
            logger.info(f'Detected xcresult bundles: {paths}')
            # TODO: Handle multiple xcresult bundles
            return XCResult(path=paths[0])

        try:
            if not kwargs.get('actions'):
                if kwargs.get('test_without_building'):
                    kwargs['actions'] = ['test-without-building']
                else:
                    kwargs['actions'] = ['test']
            super().run(**kwargs)
            return collect_xcresult()
        except Exception as e:
            xcresult = collect_xcresult()
            raise TestError(xcresult, e)

    def _derived_data_path(self, **kwargs) -> Path:
        # TODO: Run xcodebuild -showBuildSettings to get the default data path
        return Path(kwargs.get('derived_data_path') or 'DerivedData')
