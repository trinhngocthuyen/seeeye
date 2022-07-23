import subprocess
from unittest import mock

import pytest

from cicd.core.mixin.git import GitMixin


@pytest.fixture
def sut(tmp_path):
    subprocess.run(['git', '-C', tmp_path, 'init'])
    with mock.patch('os.getcwd') as mock_cwd:
        mock_cwd.return_value = tmp_path
        yield GitMixin()


def test_git_mixin_dir(sut: GitMixin, tmp_path):
    assert sut.repo.working_dir == str(tmp_path)
    assert sut.git.working_dir == str(tmp_path)
