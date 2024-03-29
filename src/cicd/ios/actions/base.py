import typing as t
from contextlib import contextmanager
from functools import cached_property
from pathlib import Path

from cicd.core.action import Action
from cicd.ios.mixin.project import ProjectMixin
from cicd.ios.syntax.xcresult import XCResult


class IOSAction(Action, ProjectMixin):
    xcresult: XCResult | None
    xcarchive_path: Path | None

    @cached_property
    def derived_data_path(self) -> Path:
        path = self.kwargs.get('derived_data_path')
        return Path(path) if path else self.metadata.default_derived_data_path

    @cached_property
    def archive_path(self) -> Path:
        path = self.kwargs.get('archive_path') or '~/Library/Developer/Xcode/Archives'
        return Path(path).expanduser()

    @contextmanager
    def collect_artifacts(
        self,
        name: str,
        base_path: Path,
        pattern: str,
        on_detected: t.Callable[[t.List[Path]], None],
        new_only=True,
    ) -> t.List[Path]:
        def find_paths() -> t.List[Path]:
            return sorted(base_path.glob(pattern), reverse=True)

        before = find_paths() if new_only else []
        try:
            yield
        finally:
            after = find_paths()
            paths = list(set(after).difference(before))
            if len(paths) == 0:
                self.logger.warning(
                    f'Cannot detect any {name} matching: {base_path / pattern}'
                )
            elif len(paths) > 1:
                self.logger.warning(f'Detected more than one {name}: {paths}')
            else:
                self.logger.info(f'Detected {name}: {paths}')
            on_detected(paths)

    @contextmanager
    def collect_xcresults(self, new_only=True) -> XCResult:
        '''Collect the xcresults generated after an action.'''

        def save(paths):
            self.xcresult = XCResult(paths[0]) if paths else None

        with self.collect_artifacts(
            name='xcresult',
            base_path=self.derived_data_path,
            pattern='Logs/Test/*.xcresult',
            on_detected=save,
            new_only=new_only,
        ):
            yield

    @contextmanager
    def collect_xcarchives(self) -> t.List[Path]:
        def save(paths):
            self.xcarchive_path = paths[0] if paths else None

        with self.collect_artifacts(
            name='xcarchive',
            base_path=self.archive_path,
            pattern='**/*.xcarchive',
            on_detected=save,
        ):
            yield
