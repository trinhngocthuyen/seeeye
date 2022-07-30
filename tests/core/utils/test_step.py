from unittest import mock

import pytest

from cicd.core.utils.step import step


@pytest.fixture
def sut(bag):
    bag.count = 0

    def tick():
        bag.count += 1
        return 0 if bag.count == 1 else 10

    bag.time.side_effect = tick
    with mock.patch('time.time', bag.time):
        yield


def test_step(sut, caplog, bag):
    with step('dummy'):
        pass

    assert caplog.messages == [
        '⇣ Step: dummy (started)',
        '⇢ Step: dummy (finished) (10 s)',
    ]
