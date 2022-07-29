from typing import List

from cicd.core.mixin.core import CoreMixin
from cicd.ios.actions.test_extraction import TestExtractionAction


class TestShardingMixin(CoreMixin):
    __test__ = False

    def extract_tests(self, **kwargs) -> List[str]:
        return TestExtractionAction(**kwargs).run()

    def test_sharding(self, **kwargs) -> List[List[str]]:
        n_shards = kwargs.get('shards', 0)
        if not n_shards:
            return []
        tests = self.extract_tests(**kwargs)
        per_shard = max(1, (len(tests) + n_shards - 1) // n_shards)
        shards = [tests[i : i + per_shard] for i in range(0, len(tests), per_shard)]
        self.logger.info(f'Shard tests into ({n_shards} shards): {shards}')
        return shards

    def get_test_shard(self, **kwargs):
        shard_idx = kwargs.get('shard_idx', 0)
        if not shard_idx:
            return []
        shard = self.test_sharding(**kwargs)[shard_idx - 1]
        self.logger.info(f'-> Test shard #{shard_idx}: {shard}')
        return shard
