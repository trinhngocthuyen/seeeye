from unittest import mock

import pytest

from cicd.ios.runner.base import Runner


@pytest.fixture
def mock_errors():
    return [RuntimeError(f'Failed on attempt #{i}') for i in range(3)]


@pytest.fixture
def mock_action_cls(bag, mock_errors):
    bag._tries = 0

    class MockAction:
        def __init__(self, **kwargs) -> None:
            pass

        def run(self):
            bag._tries += 1
            if bag._tries < 3:
                raise mock_errors[bag._tries]

    return MockAction


@pytest.fixture
def sut():
    return Runner()


def test_retries_success(sut: Runner, mock_action_cls, bag, mock_errors):
    kwargs = dict(retries=2, retry_kwargs_fn=bag.retry_kwargs_fn)
    bag.retry_kwargs_fn.return_value = kwargs
    sut.run(action_cls=mock_action_cls, **kwargs)
    bag.retry_kwargs_fn.assert_has_calls(
        [
            mock.call(kwargs, {'error': None, 'idx': 0}),
            mock.call(kwargs, {'error': mock_errors[1], 'idx': 1}),
            mock.call(kwargs, {'error': mock_errors[2], 'idx': 2}),
        ],
    )


def test_retries_error(sut: Runner, mock_action_cls):
    with pytest.raises(RuntimeError, match='Failed on attempt #2'):
        sut.run(action_cls=mock_action_cls, retries=1)
