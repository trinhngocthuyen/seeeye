import os
import shutil
import tempfile
import typing as t
from contextlib import contextmanager
from pathlib import Path

StrPath = t.Union[str, Path]


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
