from pathlib import Path
from unittest import mock

import pytest

from cicd.ios.project.metadata import Metadata


@pytest.fixture
def bag(tmp_path: Path):
    this = mock.MagicMock()
    this.xcodeproj_path = tmp_path / 'EX.xcodeproj'
    this.xcworkspace_path = tmp_path / 'EX.xcworkspace'
    this.xcodeproj_path.write_text('')
    this.xcworkspace_path.mkdir()
    with mock.patch(
        'cicd.ios.project.metadata.Metadata.workdir',
        new_callable=mock.PropertyMock,
    ) as mock_workdir:
        mock_workdir.return_value = tmp_path
        yield this


def test_project_metadata_mixin(monkeypatch, bag):
    metadata = Metadata()
    assert metadata.project_name == 'EX'
    assert metadata.xcodeproj_path == bag.xcodeproj_path
    assert metadata.xcworkspace_path == bag.xcworkspace_path
