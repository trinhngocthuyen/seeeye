from pathlib import Path

import pytest

from cicd.ios.actions.base import IOSAction


@pytest.fixture
def sut(mock_metadata_mixin):
    return IOSAction()


def test_derived_data_path(sut, bag):
    bag.metadata.default_derived_data_path = Path('default_derived_data')
    assert IOSAction().derived_data_path == Path('default_derived_data')
    assert IOSAction(
        derived_data_path='overriden_derived_data'
    ).derived_data_path == Path('overriden_derived_data')
