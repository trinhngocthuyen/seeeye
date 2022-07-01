from functools import cached_property
from pathlib import Path
from typing import Optional

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
