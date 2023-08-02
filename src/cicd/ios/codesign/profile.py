from pathlib import Path

from cicd.core.logger import logger
from cicd.core.typing import StrPath
from cicd.core.utils.file import FileUtils


class ProvisioningProfile:
    def __init__(self, path: StrPath) -> None:
        self.path = path
        self.profiles_dir = Path(
            '~/Library/MobileDevice/Provisioning Profiles'
        ).expanduser()

    def install(self):
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f'Install profile: {self.path}')
        FileUtils.copy(self.path, self.profiles_dir)
