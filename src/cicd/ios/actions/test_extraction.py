import re
import typing as t
from pathlib import Path
from shlex import quote

from cicd.core.utils.sh import sh
from cicd.ios.actions.base import IOSAction


class TestExtractionAction(IOSAction):
    '''A class to extract tests of an iOS project (after building the project).

    The extracted tests follow this format: ``<Target>/<TestCase>/<TestName>``.
    '''

    __test__ = False

    def run(self) -> t.List[str]:
        bin_paths = [
            p / p.with_suffix('').name
            for p in self.derived_data_path.glob('**/*.xctest')
        ]
        return [x for path in bin_paths for x in self._extract(bin_path=path)]

    def _extract(self, bin_path: Path) -> t.List[str]:
        result = []
        cmd = f'xcrun nm {quote(str(bin_path))} | xcrun swift-demangle | grep test'
        output = sh.exec(cmd)
        # The approach is based on this blog post
        # https://trinhngocthuyen.github.io/posts/tech/ci-extract-test-methods
        for line in output.split('\n'):
            m = re.match(r'\S+ T (\S+\.\S+\.test\S+)\(\)', line)
            if m:
                result.append(m.group(1).replace('.', '/'))
        return sorted(result)
