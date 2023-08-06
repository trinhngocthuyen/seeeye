import pytest

from cicd.ios.mixin.archive import ArchiveMixin
from cicd.ios.mixin.build import BuildMixin
from cicd.ios.mixin.test import TestMixin


@pytest.fixture
def sut_cls():
    return None


@pytest.fixture
def sut(sut_cls, mock_pre_run_and_post_run):
    return sut_cls()


@pytest.mark.parametrize(
    'sut_cls, fn_name',
    [
        (BuildMixin, 'start_building'),
        (TestMixin, 'start_testing'),
        (ArchiveMixin, 'start_archiving'),
    ],
)
def test_overall_flow(sut, fn_name, bag):
    getattr(sut, fn_name)()
    bag.pre_run.assert_called()
    bag.post_run.assert_called()
    bag.runner.run.assert_called()
