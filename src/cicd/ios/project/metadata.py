import shutil
import subprocess
from functools import cached_property
from pathlib import Path
from typing import List, Optional

from cicd.core.logger import logger


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

    @cached_property
    def xcworkspace_path(self) -> Optional[Path]:
        paths = list(self.workdir.glob('*.xcworkspace'))
        return paths[0] if paths else None

    @cached_property
    def schemes(self) -> List[str]:
        return [
            p.with_suffix('').name
            for p in self.workdir.glob('*.xcodeproj/xcshareddata/xcschemes/*.xcscheme')
        ]

    @property
    def scheme(self) -> Optional[str]:
        return self.schemes[0] if self.schemes else None

    @property
    def bundle_enabled(self) -> bool:
        return (self.workdir / 'Gemfile').exists

    def resolve_program(self, name) -> Optional[str]:
        proc = subprocess.run(['bundle', 'info', name], stdout=subprocess.DEVNULL)
        if proc.returncode == 0:
            return f'bundle exec {name}'
        if shutil.which(name):
            return name
