import re
import shutil
import typing as t
from functools import cached_property
from pathlib import Path
from shlex import quote

from cicd.core.logger import logger
from cicd.core.utils.sh import sh


class Metadata:
    @property
    def project_name(self):
        return self.xcodeproj_path.with_suffix('').name

    @property
    def workdir(self) -> Path:
        return Path()

    @cached_property
    def xcodeproj_path(self) -> Path:
        paths = list(self.workdir.glob('*.xcodeproj'))
        if len(paths) > 1:
            logger.warning('Multiple xcode projects are detected')
        return paths[0]

    @property
    def pbxproj_path(self) -> Path:
        return self.xcodeproj_path / 'project.pbxproj'

    @cached_property
    def xcworkspace_path(self) -> t.Optional[Path]:
        paths = list(self.workdir.glob('*.xcworkspace'))
        return paths[0] if paths else None

    @cached_property
    def schemes(self) -> t.List[str]:
        detected = [
            p.with_suffix('').name
            for p in self.workdir.glob('*.xcodeproj/xcshareddata/xcschemes/*.xcscheme')
        ]
        if not detected:
            logger.warning(
                'Detect no shared scheme. Please mark your scheme as shared in Xcode'
            )
        if len(detected) > 1:
            logger.warning(
                f'Detect multiple schemes: {detected}. '
                f'The first one will be chosen: {detected[0]}. '
                f'To specify the scheme, use the `-scheme` option.'
            )
        return detected

    @property
    def scheme(self) -> t.Optional[str]:
        return self.schemes[0] if self.schemes else None

    def bundle_enabled(self, name) -> bool:
        if (self.workdir / 'Gemfile').exists():
            try:
                sh.exec(f'bundle info {name}', capture_output=True)
                return True
            except:
                return False

    def resolve_program(self, name) -> t.Optional[str]:
        if self.bundle_enabled(name):
            return f'bundle exec {name}'
        if shutil.which(name):
            return name

    @cached_property
    def default_derived_data_path(self) -> Path:
        cmd = ['xcodebuild', '-showBuildSettings']
        if self.xcworkspace_path:
            cmd += ['-workspace', quote(str(self.xcworkspace_path))]
            cmd += ['-scheme', quote(self.scheme)]
        content = sh.exec(cmd)
        # Look for <path/to/Build/Products>
        m = next(re.finditer(r'\s+BUILD_ROOT = (.*)', content))
        return Path(m.group(1)).parent.parent
