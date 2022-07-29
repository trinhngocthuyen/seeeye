from unittest import mock

import pytest

from cicd.ios.mixin.test_sharding import TestShardingMixin


@pytest.fixture
def sut(bag):
    with mock.patch(
        'cicd.ios.actions.test_extraction.TestExtractionAction.run', bag.action.run
    ):
        bag.action.run.return_value = ['A1', 'A2', 'A3', 'B1', 'B2']
        yield TestShardingMixin()


def test_test_sharding(sut: TestShardingMixin, bag):
    assert sut.extract_tests() == ['A1', 'A2', 'A3', 'B1', 'B2']
    assert sut.get_test_shard(shards=2, shard_idx=1) == ['A1', 'A2', 'A3']
    assert sut.get_test_shard(shards=2, shard_idx=2) == ['B1', 'B2']
    bag.action.run.assert_called()
