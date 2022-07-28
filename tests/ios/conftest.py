from pathlib import Path

import pytest


@pytest.fixture
def mock_derived_data_path(bag, tmp_path: Path):
    bag.derived_data_path = tmp_path / 'DerivedData'
    bag.derived_data_path.mkdir(parents=True)
    return bag.derived_data_path
