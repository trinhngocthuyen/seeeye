import typing as t
from contextlib import contextmanager
from functools import cached_property
from pathlib import Path

from cicd.core.action import Action
from cicd.ios.mixin.metadata import MetadataMixin
from cicd.ios.syntax.xcresult import XCResult


class IOSAction(Action, MetadataMixin):
    xcresult: XCResult

    @cached_property
    def derived_data_path(self) -> Path:
        path = self.kwargs.get('derived_data_path')
        return Path(path) if path else self.metadata.default_derived_data_path

    def xcresult_paths(self) -> t.List[Path]:
        return sorted(self.derived_data_path.glob('Logs/Test/*.xcresult'), reverse=True)

    @contextmanager
    def collect_xcresults(self, new_only=True) -> XCResult:
        '''Collect the xcresults generated after an action.'''
        before = self.xcresult_paths() if new_only else []
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
                self.logger.warning(f'Detected more than one xcresult bundle: {paths}')
                # TODO: Merge xcresult bundles
            else:
                self.logger.info(f'Detected xcresult bundles: {paths}')
            self.xcresult = XCResult(path=paths[0])
