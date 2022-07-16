from unittest import mock

import pytest

from cicd.ios.runner.base import Runner


@pytest.fixture
def sut(bag):
    bag._tries = 0

    def run_action(**kwargs):
        bag._tries += 1
        if bag._tries < 3:
            raise RuntimeError(f'Failed on attempt #{bag._tries}')

    this = Runner()
    with mock.patch(
        'cicd.ios.runner.base.Runner.action',
        new_callable=mock.PropertyMock(return_value=bag.action),
    ):
        bag.action.run = run_action
        yield this


def test_retries_success(sut: Runner):
    sut.run(retries=2)


def test_retries_error(sut: Runner):
    with pytest.raises(RuntimeError, match='Failed on attempt #2'):
        sut.run(retries=1)
