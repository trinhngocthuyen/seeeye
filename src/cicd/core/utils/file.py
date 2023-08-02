import os
import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path

from cicd.core.typing import StrPath


class FileUtils:
    @contextmanager
    @staticmethod
    def tempdir() -> Path:
        dir = tempfile.mkdtemp()
        yield Path(dir)
        shutil.rmtree(dir, ignore_errors=True)

    @staticmethod
    def copy(src: StrPath, dst: StrPath) -> Path:
        if os.path.isdir(src):
            return Path(shutil.copytree(src, dst))
        return Path(shutil.copy(src, dst))
